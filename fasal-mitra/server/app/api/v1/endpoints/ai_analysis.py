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
        logger.error(f"Error generating AI analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI analysis: {str(e)}"
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
