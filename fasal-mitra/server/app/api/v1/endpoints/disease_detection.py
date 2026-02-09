"""
Disease Detection API Endpoints

Integrates ML-based disease detection using TensorFlow/Keras model
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
from app.services.ml_disease_service import MLDiseaseDetectionService, get_ml_disease_service
# Keep old service as fallback
from app.services.disease_service import DiseaseDetectionService, get_disease_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/detect", response_model=ResponseModel)
async def detect_disease(
    file: UploadFile = File(..., description="Image of affected crop"),
    crop_type: str = Form(..., description="Type of crop"),
    location: Optional[str] = Form(None, description="Location/State"),
    ml_service: MLDiseaseDetectionService = Depends(get_ml_disease_service)
):
    """
    Detect crop disease from uploaded image using ML model
    
    - **file**: Image file (JPG, PNG, WEBP)
    - **crop_type**: Type of crop (e.g., Rice, Wheat, Tomato, Potato, etc.)
    - **location**: Optional location for better recommendations
    
    Returns detected disease with treatment plan using TensorFlow/Keras CNN model
    
    **Supported Crops**: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach,
    Pepper (Bell), Potato, Raspberry, Soybean, Squash, Strawberry, Tomato
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
            raise HTTPException(status_code=400, detail="File must be an image (JPG, PNG, WEBP)")
        
        # Validate file size (max 10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        file_size = 0
        
        # Read image
        image_data = await file.read()
        file_size = len(image_data)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({file_size/1024/1024:.1f}MB) exceeds maximum allowed size (10MB)"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        logger.info(f"Processing disease detection: crop={crop_type}, size={file_size/1024:.1f}KB, location={location}")
        
        # Detect disease using ML model
        result = await ml_service.detect_disease(
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
            message="Disease detection completed using ML model",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Disease detection failed: {str(e)}"
        )
            message="Disease detected successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases", response_model=ResponseModel)
async def list_diseases(
    crop_type: Optional[str] = None,
    ml_service: MLDiseaseDetectionService = Depends(get_ml_disease_service)
):
    """
    List all known diseases from ML model database
    
    - **crop_type**: Optional filter by crop type (e.g., Tomato, Potato, Apple)
    
    Returns list of known diseases with causes and treatments
    """
    diseases = ml_service.get_all_diseases(crop_type=crop_type)
    
    return ResponseModel(
        success=True,
        message=f"Found {len(diseases)} diseases" + (f" for {crop_type}" if crop_type else ""),
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


@router.get("/supported-crops", response_model=ResponseModel)
async def get_supported_crops(
    ml_service: MLDiseaseDetectionService = Depends(get_ml_disease_service)
):
    """
    Get list of crops supported by the ML model
    
    Returns list of crop names that can be analyzed
    """
    crops = ml_service.get_supported_crops()
    
    return ResponseModel(
        success=True,
        message=f"Model supports {len(crops)} crop types",
        data={
            "crops": crops,
            "total": len(crops)
        }
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
