"""
AI-powered crop analysis endpoints using Gemini API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.config import settings
from app.models.common import ResponseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Lazy load Gemini client
_genai_client = None


def generate_fallback_analysis(crop: str, state: str, season: str, month: str) -> str:
    """Generate a fallback analysis when API quota is exceeded"""
    return f"""**1. Suitability Analysis:**
{crop.title()} is commonly cultivated in {state} during the {season} season. The {month} timing is generally favorable for this crop in the region. Consider local soil conditions and water availability before proceeding.

**2. Key Benefits:**
- Well-suited to the local climate and soil conditions of {state}
- Good market demand during this growing season
- Established cultivation practices available from local agricultural experts

**3. Important Risks & Challenges:**
- Weather variability may affect crop yield - maintain weather monitoring
- Pest and disease pressure during {season} - implement integrated pest management
- Water management is critical - ensure adequate irrigation facilities

**4. Recommendations:**
- Consult with local agricultural extension officers for region-specific advice
- Use certified seeds from reliable sources for better germination
- Implement soil testing to determine fertilizer requirements
- Plan for proper drainage and irrigation based on {season} rainfall patterns

**5. Expected Timeline:**
Typical {crop.title()} cultivation cycle for {season} season:
- Land preparation: 2-3 weeks before sowing
- Sowing period: Early {month}
- Growth phase: 60-90 days depending on variety
- Harvest: Varies by crop variety and local conditions

*Note: This is general guidance. For detailed AI-powered analysis, please try again later when service is available.*"""


def get_genai_client():
    global _genai_client
    if _genai_client is None and settings.GEMINI_API_KEY:
        try:
            from google import genai
            _genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            logger.info("✅ Gemini API client initialized for crop analysis")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            _genai_client = None
    return _genai_client


class CropAnalysisRequest(BaseModel):
    crop: str
    country: Optional[str] = None
    state: str
    district: Optional[str] = None
    month_name: str
    season: str
    land_size: Optional[float] = None


@router.post("/crop-analysis", response_model=ResponseModel)
async def generate_crop_analysis(request: CropAnalysisRequest):
    """
    Generate AI-powered crop analysis using Gemini
    """
    try:
        if not settings.GEMINI_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="AI analysis service is not configured. Please set GEMINI_API_KEY."
            )

        client = get_genai_client()
        if not client:
            raise HTTPException(
                status_code=503,
                detail="Failed to initialize Gemini AI client"
            )
        
        # Build the prompt
        prompt = f"""You are an agricultural expert. Provide a detailed analysis for growing {request.crop} in the following conditions:

**Location Details:**
- Country: {request.country or 'Not specified'}
- State: {request.state}
- District: {request.district or 'Not specified'}
- Month: {request.month_name}
- Season: {request.season}
- Land Size: {request.land_size if request.land_size else 'Not specified'} hectares

Provide analysis in the following format:

**1. Suitability Analysis:**
(In 2-3 simple sentences, explain if this crop is suitable for this region and season)

**2. Key Benefits:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**3. Important Risks & Challenges:**
- [Risk 1 with brief solution]
- [Risk 2 with brief solution]
- [Risk 3 with brief solution]

**4. Recommendations:**
(Provide 2-3 practical tips for success)

**5. Expected Timeline:**
(Brief overview of sowing to harvesting period)

Keep the language simple and easy to understand for farmers. Use shorter sentences and practical advice."""

        # Generate content using new SDK
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if not response or not response.text:
            raise HTTPException(
                status_code=500,
                detail="AI model returned empty response"
            )

        return ResponseModel(
            success=True,
            message="AI analysis generated successfully",
            data={
                "analysis": response.text,
                "crop": request.crop,
                "location": f"{request.state}, {request.country or 'India'}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        error_str = str(e)
        logger.error(f"Error generating AI analysis: {error_str}")
        
        # Handle quota exhausted errors - use fallback response
        if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
            logger.warning("API quota exceeded, using fallback analysis")
            fallback_text = generate_fallback_analysis(
                request.crop,
                request.state,
                request.season,
                request.month_name
            )
            return ResponseModel(
                success=True,
                message="AI analysis generated (fallback mode)",
                data={
                    "analysis": fallback_text,
                    "crop": request.crop,
                    "location": f"{request.state}, {request.country or 'India'}",
                    "fallback": True
                }
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI analysis: {error_str}"
        )


@router.get("/health", response_model=ResponseModel)
async def check_ai_service_health():
    """
    Check if AI analysis service is available
    """
    is_available = bool(settings.GEMINI_API_KEY)
    
    return ResponseModel(
        success=True,
        message="AI service health check",
        data={
            "available": is_available,
            "model": "gemini-2.5-flash" if is_available else None
        }
    )
