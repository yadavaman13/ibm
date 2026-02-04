"""
Health check and system info endpoints
"""

from fastapi import APIRouter, Depends
from app.models.common import HealthResponse, ResponseModel
from app.config import settings
from app.core.data_loader import get_data_loader, DataLoader
from datetime import datetime
import sys

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns the current status of the API
    """
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version=settings.APP_VERSION,
        timestamp=datetime.now()
    )


@router.get("/info")
async def system_info(data_loader: DataLoader = Depends(get_data_loader)):
    """
    Get system information including available data
    
    Returns:
        - System version
        - Python version
        - Available crops, states, seasons
        - Dataset statistics
    """
    # Get dataset info
    dataset_info = data_loader.get_dataset_info()
    
    return ResponseModel(
        success=True,
        message="System information retrieved",
        data={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "datasets": dataset_info,
            "features": {
                "disease_detection": True,
                "yield_prediction": True,
                "yield_gap_analysis": True,
                "multi_scenario": True,
                "weather_forecast": True,
                "soil_analysis": True,
                "chatbot": settings.GEMINI_API_KEY != "",
                "translation": True
            }
        }
    )


@router.get("/stats")
async def get_statistics(data_loader: DataLoader = Depends(get_data_loader)):
    """
    Get statistical information about the datasets
    
    Returns summary statistics about available data
    """
    info = data_loader.get_dataset_info()
    
    stats = {
        "total_records": info.get("records", {}),
        "available_crops": len(info.get("available_crops", [])),
        "available_states": len(info.get("available_states", [])),
        "available_seasons": len(info.get("available_seasons", [])),
        "crops_list": info.get("available_crops", [])[:10],  # First 10 crops
        "states_list": info.get("available_states", [])[:10],  # First 10 states
        "seasons_list": info.get("available_seasons", [])
    }
    
    return ResponseModel(
        success=True,
        message="Statistics retrieved",
        data=stats
    )
