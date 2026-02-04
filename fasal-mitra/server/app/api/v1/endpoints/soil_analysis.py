"""
Soil Analysis API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
import logging

from app.models.common import ResponseModel
from app.services.soil_service import SoilAnalysisService, get_soil_service

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
    service: SoilAnalysisService = Depends(get_soil_service)
):
    """
    Check soil suitability for a specific crop
    
    - **state**: State name
    - **crop**: Crop name
    
    Returns suitability analysis with recommendations
    """
    try:
        result = service.check_suitability(state=state, crop=crop)
        
        return ResponseModel(
            success=True,
            message="Suitability analysis completed",
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
