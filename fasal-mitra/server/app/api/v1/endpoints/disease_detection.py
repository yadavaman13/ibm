"""
Disease Detection API Endpoints
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import Optional, List
import uuid
from datetime import datetime
import logging

from app.models.disease import (
    DiseaseDetectionRequest,
    DiseaseDetectionResponse,
    DiseaseInfo,
    TreatmentPlan,
    SeverityLevel,
    DiseaseHistoryItem
)
from app.models.common import ResponseModel
from app.services.disease_service import DiseaseDetectionService, get_disease_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/detect", response_model=ResponseModel)
async def detect_disease(
    file: UploadFile = File(..., description="Image of affected crop"),
    crop_type: str = Form(..., description="Type of crop"),
    location: Optional[str] = Form(None, description="Location/State"),
    service: DiseaseDetectionService = Depends(get_disease_service)
):
    """
    Detect crop disease from uploaded image
    
    - **file**: Image file (JPG, PNG, WEBP)
    - **crop_type**: Type of crop (e.g., Rice, Wheat, Cotton)
    - **location**: Optional location for better recommendations
    
    Returns detected disease with treatment plan
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        image_data = await file.read()
        
        # Detect disease
        result = await service.detect_disease(
            image_data=image_data,
            crop_type=crop_type,
            location=location
        )
        
        return ResponseModel(
            success=True,
            message="Disease detected successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases", response_model=ResponseModel)
async def list_diseases(
    crop_type: Optional[str] = None,
    service: DiseaseDetectionService = Depends(get_disease_service)
):
    """
    List all known diseases
    
    - **crop_type**: Optional filter by crop type
    
    Returns list of known diseases
    """
    diseases = service.get_all_diseases(crop_type=crop_type)
    
    return ResponseModel(
        success=True,
        message=f"Found {len(diseases)} diseases",
        data=diseases
    )


@router.get("/history", response_model=ResponseModel)
async def get_detection_history(
    limit: int = 10,
    service: DiseaseDetectionService = Depends(get_disease_service)
):
    """
    Get detection history (placeholder for future implementation)
    
    Returns recent disease detections
    """
    return ResponseModel(
        success=True,
        message="History retrieved",
        data={
            "history": [],
            "total": 0,
            "note": "History tracking will be implemented with database integration"
        }
    )
