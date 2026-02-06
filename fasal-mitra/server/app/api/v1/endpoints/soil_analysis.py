"""
Soil Analysis API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query, File, UploadFile, Form
from typing import Optional
import logging

from app.models.common import ResponseModel
from app.services.soil_service import SoilAnalysisService, get_soil_service
from app.services.image_analysis_service import ImageAnalysisService, get_image_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/data/{state}", response_model=ResponseModel)
async def get_soil_data(
    state: str,
    service: SoilAnalysisService = Depends(get_soil_service)
):
    """
    Get soil data for a specific state
    
    - **state**: State name (e.g., Punjab, Maharashtra)
    
    Returns soil composition (N, P, K, pH) for the state
    """
    try:
        result = service.get_soil_data(state=state)
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"No soil data found for state: {state}")
        
        return ResponseModel(
            success=True,
            message=f"Soil data retrieved for {state}",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving soil data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suitability", response_model=ResponseModel)
async def check_soil_suitability(
    state: str = Query(..., description="State name"),
    crop: str = Query(..., description="Crop name"),
    field_size: Optional[float] = Query(None, description="Field size in hectares"),
    irrigation_type: Optional[str] = Query(None, description="Irrigation type"),
    previous_crop: Optional[str] = Query(None, description="Previous crop"),
    water_quality: Optional[str] = Query(None, description="Water source quality"),

    service: SoilAnalysisService = Depends(get_soil_service)
):
    """
    Enhanced soil suitability check with additional farming parameters
    
    - **state**: State name
    - **crop**: Crop name
    - **field_size**: Field size in hectares (optional)
    - **irrigation_type**: rainfed, drip, sprinkler, flood, mixed (optional)
    - **previous_crop**: Previous crop grown (optional)
    - **water_quality**: sweet, slightlySalty, verySalty, unknown (optional)

    
    Returns enhanced suitability analysis with actionable recommendations
    """
    try:
        enhanced_params = {
            "field_size": field_size,
            "irrigation_type": irrigation_type,
            "previous_crop": previous_crop,
            "water_quality": water_quality
        }
        
        result = service.check_enhanced_suitability(
            state=state, 
            crop=crop,
            **enhanced_params
        )
        
        return ResponseModel(
            success=True,
            message="Enhanced suitability analysis completed",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in suitability check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations/{state}", response_model=ResponseModel)
async def get_crop_recommendations(
    state: str,
    service: SoilAnalysisService = Depends(get_soil_service)
):
    """
    Get crop recommendations based on soil composition
    
    - **state**: State name
    
    Returns recommended crops for the state's soil
    """
    try:
        result = service.get_crop_recommendations(state=state)
        
        return ResponseModel(
            success=True,
            message="Crop recommendations generated",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/states", response_model=ResponseModel)
async def get_available_states(service: SoilAnalysisService = Depends(get_soil_service)):
    """Get list of states with soil data"""
    states = service.get_available_states()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(states)} states",
        data={"states": states}
    )


@router.post("/analyze-image", response_model=ResponseModel)
async def analyze_soil_image(
    image: UploadFile = File(..., description="Soil image file"),
    state: str = Form(..., description="State name"),
    crop: str = Form(..., description="Crop name"),
    field_size: Optional[float] = Form(None, description="Field size in hectares"),
    irrigation_type: Optional[str] = Form(None, description="Irrigation type"),
    previous_crop: Optional[str] = Form(None, description="Previous crop"),
    water_quality: Optional[str] = Form(None, description="Water quality"),

    soil_service: SoilAnalysisService = Depends(get_soil_service),
    image_service: ImageAnalysisService = Depends(get_image_service)
):
    """
    Comprehensive soil analysis combining image analysis with traditional soil testing data
    
    - **image**: Soil image file (JPG, PNG, etc.)
    - **state**: State name for soil data lookup
    - **crop**: Target crop for analysis
    - **field_size**: Field size in hectares (optional)
    - **irrigation_type**: Irrigation method (optional)
    - **previous_crop**: Previous crop grown (optional) 
    - **water_quality**: Water source quality (optional)

    
    Returns comprehensive analysis combining visual soil assessment with lab data
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Check file size (max 10MB)
        contents = await image.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image size must be under 10MB")
        
        # Reset file pointer for image analysis
        await image.seek(0)
        
        logger.info(f"Starting image analysis for soil sample from {state}")
        
        # Analyze image using OpenAI Vision
        image_analysis = await image_service.analyze_soil_image(image)
        
        # Get traditional soil analysis
        enhanced_params = {
            "field_size": field_size,
            "irrigation_type": irrigation_type,
            "previous_crop": previous_crop,
            "water_quality": water_quality
        }
        
        traditional_analysis = soil_service.check_enhanced_suitability(
            state=state,
            crop=crop,
            **enhanced_params
        )
        
        # Combine image analysis with traditional analysis
        combined_analysis = await image_service.combine_analyses(
            image_analysis=image_analysis,
            traditional_analysis=traditional_analysis,
            state=state,
            crop=crop
        )
        
        return ResponseModel(
            success=True,
            message="Image-enhanced soil analysis completed successfully",
            data={
                "image_analysis": image_analysis,
                "traditional_analysis": traditional_analysis,
                "combined_analysis": combined_analysis,
                "analysis_type": "image_enhanced"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in image-based soil analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")
