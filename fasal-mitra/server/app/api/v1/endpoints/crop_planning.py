"""
Crop Planning API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.services.crop_planning_service import CropPlanningService, get_crop_planning_service
from app.models.common import ResponseModel

router = APIRouter()
logger = logging.getLogger(__name__)


class CropPlanningRequest(BaseModel):
    """Request model for crop planning"""
    state: str = Field(..., description="State name (e.g., Punjab, Maharashtra)")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month (1-12), auto-detected if not provided")
    land_size: Optional[float] = Field(None, gt=0, description="Total land size in hectares")
    latitude: Optional[float] = Field(None, description="Latitude for weather forecast")
    longitude: Optional[float] = Field(None, description="Longitude for weather forecast")
    
    class Config:
        json_schema_extra = {
            "example": {
                "state": "Punjab",
                "month": 7,
                "land_size": 5.0,
                "latitude": 30.7333,
                "longitude": 76.7794
            }
        }


@router.post("/plan", response_model=ResponseModel)
async def plan_crops(
    request: CropPlanningRequest,
    service: CropPlanningService = Depends(get_crop_planning_service)
):
    """
    Get crop recommendations based on:
    - Location (state)
    - Current season (month)
    - Land size (optional, for quantity estimation)
    - Weather forecast (optional, if coordinates provided)
    
    Returns top 3 recommended crops with:
    - Final score
    - Market trend analysis
    - Weather suitability
    - Risk assessment
    - Quantity recommendations
    - Detailed reasoning
    
    **Safety Notice**: This is AI-based guidance. Always consult local agriculture officers.
    """
    try:
        logger.info(f"Crop planning request: state={request.state}, month={request.month}")
        
        result = await service.plan_crops(
            state=request.state,
            month=request.month,
            land_size=request.land_size,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        if not result.get("success", False):
            return ResponseModel(
                success=False,
                message=result.get("message", "Failed to generate crop recommendations"),
                data=None
            )
        
        return ResponseModel(
            success=True,
            message="Crop recommendations generated successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in crop planning: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Crop planning failed: {str(e)}"
        )


@router.get("/seasons")
async def get_seasons(
    service: CropPlanningService = Depends(get_crop_planning_service)
):
    """
    Get information about all crop seasons and their timing
    """
    try:
        seasons_data = service.get_all_seasons()
        
        return ResponseModel(
            success=True,
            message="Season information retrieved from historical data",
            data=seasons_data
        )
    except Exception as e:
        logger.error(f"Error fetching seasons: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops/{crop_name}")
async def get_crop_details(
    crop_name: str,
    service: CropPlanningService = Depends(get_crop_planning_service)
):
    """
    Get detailed requirements and information for a specific crop from historical data
    """
    try:
        crop_info = service.get_crop_details(crop_name)
        
        if "error" in crop_info:
            return ResponseModel(
                success=False,
                message=crop_info["error"],
                data=None
            )
        
        return ResponseModel(
            success=True,
            message=f"Details for {crop_name} from {crop_info.get('historical_stats', {}).get('total_records', 0)} historical records",
            data=crop_info
        )
    
    except Exception as e:
        logger.error(f"Error fetching crop details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-prices/{crop_name}")
async def get_market_prices(
    crop_name: str,
    state: Optional[str] = None,
    service: CropPlanningService = Depends(get_crop_planning_service)
):
    """
    Get real market prices for a crop from government Agmarknet data
    """
    try:
        prices_data = service.get_market_prices(crop_name, state)
        
        if "error" in prices_data:
            return ResponseModel(
                success=False,
                message=prices_data["error"],
                data=None
            )
        
        if not prices_data.get("recent_prices"):
            return ResponseModel(
                success=False,
                message=f"No market data found for {crop_name}",
                data=None
            )
        
        return ResponseModel(
            success=True,
            message=f"Real market prices for {crop_name} from {prices_data['total_records']} mandi records",
            data=prices_data
        )
    
    except Exception as e:
        logger.error(f"Error fetching market prices: {e}")
        raise HTTPException(status_code=500, detail=str(e))
