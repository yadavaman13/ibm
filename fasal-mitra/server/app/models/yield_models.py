"""
Pydantic models for Yield Prediction API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Season(str, Enum):
    """Agricultural seasons"""
    KHARIF = "Kharif"
    RABI = "Rabi"
    SUMMER = "Summer"
    WHOLE_YEAR = "Whole Year"
    AUTUMN = "Autumn"
    WINTER = "Winter"


class YieldPredictionRequest(BaseModel):
    """Request model for yield prediction"""
    crop: str = Field(..., description="Crop name", example="Rice")
    state: str = Field(..., description="State name", example="Punjab")
    season: str = Field(..., description="Season", example="Kharif")
    area: float = Field(..., gt=0, description="Area in hectares", example=100.0)
    fertilizer: float = Field(..., ge=0, description="Fertilizer in kg/ha", example=25000.0)
    pesticide: float = Field(..., ge=0, description="Pesticide in kg/ha", example=500.0)
    
    # Optional weather parameters
    avg_temp_c: Optional[float] = Field(None, description="Average temperature in Celsius")
    total_rainfall_mm: Optional[float] = Field(None, description="Total rainfall in mm")
    avg_humidity_percent: Optional[float] = Field(None, description="Average humidity percentage")


class YieldPredictionResponse(BaseModel):
    """Response model for yield prediction"""
    prediction_id: str
    timestamp: datetime
    input_params: YieldPredictionRequest
    predicted_yield: float = Field(..., description="Predicted yield in tons/hectare")
    confidence_interval: Dict[str, float] = Field(..., description="Lower and upper bounds")
    factors_affecting: List[Dict[str, Any]]
    recommendations: List[str]
    model_confidence: float = Field(..., ge=0.0, le=1.0)


class YieldGapRequest(BaseModel):
    """Request for yield gap analysis"""
    crop: str
    state: str
    season: Optional[str] = None
    current_yield: float = Field(..., gt=0, description="Current yield in tons/hectare")


class YieldGapResponse(BaseModel):
    """Response for yield gap analysis"""
    analysis_id: str
    timestamp: datetime
    current_yield: float
    benchmarks: Dict[str, float]
    gaps: Dict[str, float]
    percentile_rank: float
    improvement_potential: float
    recommendations: List[str]
    top_performers_characteristics: Dict[str, Any]


class BenchmarkRequest(BaseModel):
    """Request for yield benchmarks"""
    crop: str
    state: str
    season: Optional[str] = None


class BenchmarkResponse(BaseModel):
    """Response for yield benchmarks"""
    crop: str
    state: str
    season: Optional[str]
    total_records: int
    years_covered: str
    average_yield: float
    median_yield: float
    top_10_percent: float
    top_25_percent: float
    max_yield_achieved: float
    yield_std: float
