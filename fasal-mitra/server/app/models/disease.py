"""
Pydantic models for Disease Detection API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class SeverityLevel(str, Enum):
    """Disease severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class DiseaseDetectionRequest(BaseModel):
    """Request model for disease detection"""
    crop_type: str = Field(..., description="Type of crop", example="Rice")
    location: Optional[str] = Field(None, description="Location/state", example="Punjab")
    additional_symptoms: Optional[str] = Field(None, description="Additional symptoms described by farmer")


class TreatmentPlan(BaseModel):
    """Treatment plan for a disease"""
    treatments: List[str]
    cost_estimate: int = Field(..., description="Estimated cost in INR")


class DiseaseInfo(BaseModel):
    """Information about detected disease"""
    disease_id: str
    name: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    severity: SeverityLevel
    symptoms: List[str]
    causes: List[str]
    treatments: Dict[str, TreatmentPlan]
    prevention: List[str]
    crops_affected: List[str]


class DiseaseDetectionResponse(BaseModel):
    """Response model for disease detection"""
    detection_id: str
    timestamp: datetime
    crop_type: str
    location: Optional[str]
    detected_disease: DiseaseInfo
    recommendations: List[str]
    estimated_severity: SeverityLevel
    treatment_plan: TreatmentPlan
    next_steps: List[str]


class DiseaseHistoryItem(BaseModel):
    """History item for disease detection"""
    detection_id: str
    timestamp: datetime
    crop_type: str
    disease_name: str
    severity: SeverityLevel
    image_url: Optional[str]
