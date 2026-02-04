"""
Pydantic models for Weather API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, date


class WeatherRequest(BaseModel):
    """Request model for weather data"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")


class CurrentWeatherResponse(BaseModel):
    """Response model for current weather"""
    latitude: float
    longitude: float
    location_name: Optional[str] = None
    temperature: float = Field(..., description="Temperature in °C")
    humidity: float = Field(..., description="Relative humidity in %")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    precipitation: float = Field(..., description="Precipitation in mm")
    weather_code: int
    weather_description: str
    observation_time: datetime
    recommendations: List[str] = Field(default_factory=list)


class DailyForecast(BaseModel):
    """Daily weather forecast"""
    date: date
    temp_max: float
    temp_min: float
    precipitation_sum: float
    wind_speed_max: float
    weather_code: int
    weather_description: str


class ForecastRequest(BaseModel):
    """Request for weather forecast"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    days: int = Field(default=7, ge=1, le=16, description="Number of forecast days")


class ForecastResponse(BaseModel):
    """Response for weather forecast"""
    latitude: float
    longitude: float
    location_name: Optional[str]
    forecast: List[DailyForecast]
    farming_recommendations: List[str]
    alerts: List[str] = Field(default_factory=list)


class LocationResponse(BaseModel):
    """Response for location name from coordinates"""
    latitude: float
    longitude: float
    location_name: str
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
