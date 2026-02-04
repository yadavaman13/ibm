"""
Weather API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import Optional
import logging

from app.models.weather import (
    WeatherRequest,
    CurrentWeatherResponse,
    ForecastRequest,
    ForecastResponse,
    LocationResponse
)
from app.models.common import ResponseModel
from app.services.weather_service import WeatherServiceAPI, get_weather_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/current", response_model=ResponseModel)
async def get_current_weather(
    request: WeatherRequest,
    service: WeatherServiceAPI = Depends(get_weather_service)
):
    """
    Get current weather for a location
    
    - **latitude**: Latitude coordinate (-90 to 90)
    - **longitude**: Longitude coordinate (-180 to 180)
    
    Returns current weather conditions with farming recommendations
    """
    try:
        result = await service.get_current_weather(
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        return ResponseModel(
            success=True,
            message="Current weather retrieved",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error fetching current weather: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forecast", response_model=ResponseModel)
async def get_weather_forecast(
    request: ForecastRequest,
    service: WeatherServiceAPI = Depends(get_weather_service)
):
    """
    Get weather forecast for next N days
    
    - **latitude**: Latitude coordinate
    - **longitude**: Longitude coordinate
    - **days**: Number of forecast days (1-16, default: 7)
    
    Returns daily forecast with farming recommendations
    """
    try:
        result = await service.get_forecast(
            latitude=request.latitude,
            longitude=request.longitude,
            days=request.days
        )
        
        return ResponseModel(
            success=True,
            message=f"{request.days}-day forecast retrieved",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error fetching weather forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/{lat}/{lon}", response_model=ResponseModel)
async def get_location_name(
    lat: float = Path(..., ge=-90, le=90),
    lon: float = Path(..., ge=-180, le=180),
    service: WeatherServiceAPI = Depends(get_weather_service)
):
    """
    Get location name from coordinates (reverse geocoding)
    
    - **lat**: Latitude
    - **lon**: Longitude
    
    Returns location name, state, country
    """
    try:
        result = service.get_location_name(latitude=lat, longitude=lon)
        
        return ResponseModel(
            success=True,
            message="Location retrieved",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error getting location name: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
