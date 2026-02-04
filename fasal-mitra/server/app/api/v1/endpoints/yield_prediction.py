"""
Yield Prediction API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from app.models.yield_models import (
    YieldPredictionRequest,
    YieldPredictionResponse,
    YieldGapRequest,
    YieldGapResponse,
    BenchmarkRequest,
    BenchmarkResponse
)
from app.models.common import ResponseModel
from app.services.yield_service import YieldPredictionService, get_yield_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=ResponseModel)
async def predict_yield(
    request: YieldPredictionRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Predict crop yield based on input parameters
    
    - **crop**: Crop name (e.g., Rice, Wheat)
    - **state**: State name (e.g., Punjab, Maharashtra)
    - **season**: Season (Kharif, Rabi, Summer, etc.)
    - **area**: Cultivated area in hectares
    - **fertilizer**: Fertilizer amount in kg/ha
    - **pesticide**: Pesticide amount in kg/ha
    
    Returns predicted yield with confidence interval
    """
    try:
        result = await service.predict_yield(request)
        
        return ResponseModel(
            success=True,
            message="Yield predicted successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in yield prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gap-analysis", response_model=ResponseModel)
async def analyze_yield_gap(
    request: YieldGapRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Analyze yield gap compared to benchmarks
    
    Compares farmer's current yield with:
    - Average yields in the region
    - Top 25% performers
    - Top 10% performers
    - Maximum achieved yield
    
    Returns gap analysis with improvement recommendations
    """
    try:
        result = await service.analyze_yield_gap(request)
        
        return ResponseModel(
            success=True,
            message="Yield gap analyzed successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in yield gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/benchmarks", response_model=ResponseModel)
async def get_yield_benchmarks(
    request: BenchmarkRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Get yield benchmarks for a crop in a specific region
    
    Returns statistical benchmarks including:
    - Average, median, max yields
    - Top performer thresholds
    - Historical trends
    """
    try:
        result = service.get_benchmarks(request)
        
        return ResponseModel(
            success=True,
            message="Benchmarks retrieved successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error retrieving benchmarks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops", response_model=ResponseModel)
async def get_available_crops(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available crops"""
    crops = service.get_available_crops()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(crops)} crops",
        data={"crops": crops}
    )


@router.get("/states", response_model=ResponseModel)
async def get_available_states(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available states"""
    states = service.get_available_states()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(states)} states",
        data={"states": states}
    )


@router.get("/seasons", response_model=ResponseModel)
async def get_available_seasons(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available seasons"""
    seasons = service.get_available_seasons()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(seasons)} seasons",
        data={"seasons": seasons}
    )
