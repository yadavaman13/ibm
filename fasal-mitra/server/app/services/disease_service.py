"""
Disease Detection Service

Ports logic from src/features/crop_disease_detector.py
"""

import numpy as np
import random
from datetime import datetime
from typing import Optional, Dict, List
import uuid
import logging
from functools import lru_cache
from PIL import Image
import io

from app.models.disease import (
    DiseaseDetectionResponse,
    DiseaseInfo,
    TreatmentPlan,
    SeverityLevel
)

logger = logging.getLogger(__name__)


class DiseaseDetectionService:
    """AI-powered crop disease detection service"""
    
    def __init__(self):
        self.disease_database = self._initialize_disease_database()
    
    def _initialize_disease_database(self) -> Dict:
        """Initialize comprehensive disease database"""
        return {
            'leaf_spot': {
                'name': 'Leaf Spot Disease',
                'crops_affected': ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato'],
                'symptoms': ['Brown/black spots on leaves', 'Yellowing around spots', 'Premature leaf drop'],
                'causes': ['Fungal infection', 'High humidity', 'Poor air circulation'],
                'severity_indicators': {
                    'mild': 'Few scattered spots (1-5% leaf area)',
                    'moderate': 'Multiple spots covering 5-25% leaf area',
                    'severe': 'Extensive spotting >25% leaf area, leaf yellowing'
                },
                'treatments': {
                    'mild': ['Copper-based fungicide spray', 'Improve air circulation', 'Remove affected leaves'],
                    'moderate': ['Systemic fungicide (Propiconazole)', 'Weekly spraying for 3 weeks', 'Reduce irrigation frequency'],
                    'severe': ['Immediate fungicide treatment', 'Remove severely affected plants', 'Soil treatment with beneficial microbes']
                },
                'prevention': [
                    'Crop rotation with non-host crops',
                    'Proper spacing for air circulation',
                    'Avoid overhead irrigation',
                    'Regular field sanitation',
                    'Use resistant varieties'
                ],
                'cost_estimate': {'mild': 500, 'moderate': 1500, 'severe': 3000}
            },
            'bacterial_blight': {
                'name': 'Bacterial Blight',
                'crops_affected': ['Rice', 'Cotton', 'Beans', 'Citrus'],
                'symptoms': ['Water-soaked lesions', 'Yellow halos around spots', 'Wilting of leaves'],
                'causes': ['Bacterial infection', 'Wounds from insects/tools', 'Wet conditions'],
                'treatments': {
                    'mild': ['Copper hydroxide spray', 'Remove infected debris', 'Improve drainage'],
                    'moderate': ['Streptomycin antibiotic', 'Copper-based bactericide', 'Enhanced sanitation'],
                    'severe': ['Immediate plant removal', 'Soil sterilization', 'Quarantine affected area']
                },
                'prevention': [
                    'Use certified disease-free seeds',
                    'Sterilize tools between plants',
                    'Avoid working in wet conditions',
                    'Control insect vectors'
                ],
                'cost_estimate': {'mild': 800, 'moderate': 2000, 'severe': 4000}
            },
            'powdery_mildew': {
                'name': 'Powdery Mildew',
                'crops_affected': ['Wheat', 'Barley', 'Cotton', 'Grapes', 'Cucumber'],
                'symptoms': ['White powdery coating on leaves', 'Stunted growth', 'Reduced yield'],
                'causes': ['Fungal spores', 'High humidity with dry conditions'],
                'treatments': {
                    'mild': ['Sulfur-based spray', 'Baking soda solution (1%)', 'Improve air flow'],
                    'moderate': ['Systemic fungicide (Myclobutanil)', 'Weekly applications', 'Remove infected leaves'],
                    'severe': ['Triazole fungicides', 'Destroy heavily infected plants', 'Soil treatment']
                },
                'prevention': [
                    'Plant resistant varieties',
                    'Ensure proper plant spacing',
                    'Avoid late evening irrigation'
                ],
                'cost_estimate': {'mild': 400, 'moderate': 1200, 'severe': 2500}
            }
        }
    
    async def detect_disease(
        self,
        image_data: bytes,
        crop_type: str,
        location: Optional[str] = None
    ) -> Dict:
        """
        Detect disease from image
        
        For now, this is simulated detection. In production, this would use
        a computer vision model (TensorFlow/PyTorch).
        """
        try:
            # Validate image
            image = Image.open(io.BytesIO(image_data))
            logger.info(f"Processing image: {image.size}, format: {image.format}")
            
            # Simulate AI detection (in production, use ML model)
            detected_disease_id, confidence, severity = self._simulate_detection(crop_type)
            
            disease_data = self.disease_database[detected_disease_id]
            
            # Create disease info
            disease_info = DiseaseInfo(
                disease_id=detected_disease_id,
                name=disease_data['name'],
                confidence=confidence,
                severity=severity,
                symptoms=disease_data['symptoms'],
                causes=disease_data['causes'],
                treatments={
                    sev: TreatmentPlan(
                        treatments=treatments,
                        cost_estimate=disease_data['cost_estimate'][sev]
                    )
                    for sev, treatments in disease_data['treatments'].items()
                },
                prevention=disease_data['prevention'],
                crops_affected=disease_data['crops_affected']
            )
            
            # Generate response
            response = {
                "detection_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "crop_type": crop_type,
                "location": location,
                "detected_disease": disease_info.dict(),
                "estimated_severity": severity,
                "treatment_plan": {
                    "treatments": disease_data['treatments'][severity],
                    "cost_estimate": disease_data['cost_estimate'][severity]
                },
                "recommendations": self._generate_recommendations(disease_data, severity, crop_type),
                "next_steps": self._generate_next_steps(severity)
            }
            
            return response
        
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            raise
    
    def _simulate_detection(self, crop_type: str) -> tuple:
        """Simulate AI detection (replace with real ML model)"""
        # Select a random disease
        diseases = list(self.disease_database.keys())
        disease_id = random.choice(diseases)
        
        # Random confidence and severity
        confidence = round(random.uniform(0.75, 0.98), 2)
        severity = random.choice([SeverityLevel.MILD, SeverityLevel.MODERATE, SeverityLevel.SEVERE])
        
        return disease_id, confidence, severity
    
    def _generate_recommendations(self, disease_data: Dict, severity: str, crop_type: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = [
            f"Immediately inspect entire {crop_type} field for similar symptoms",
            "Document affected area size and location",
            f"Expected treatment cost: ₹{disease_data['cost_estimate'][severity]}"
        ]
        
        if severity == SeverityLevel.SEVERE:
            recommendations.append("⚠️ Urgent action required - consult agricultural expert")
        
        return recommendations
    
    def _generate_next_steps(self, severity: str) -> List[str]:
        """Generate next steps based on severity"""
        if severity == SeverityLevel.MILD:
            return [
                "Monitor daily for progression",
                "Apply recommended treatment within 48 hours",
                "Keep infected area isolated"
            ]
        elif severity == SeverityLevel.MODERATE:
            return [
                "Begin treatment immediately",
                "Monitor twice daily",
                "Consider consulting local agricultural expert",
                "Quarantine affected plants"
            ]
        else:  # SEVERE
            return [
                "⚠️ Emergency action - treat within 24 hours",
                "Contact agricultural extension officer",
                "Consider removing severely affected plants",
                "Prevent spread to adjacent fields"
            ]
    
    def get_all_diseases(self, crop_type: Optional[str] = None) -> List[Dict]:
        """Get all known diseases, optionally filtered by crop"""
        diseases = []
        
        for disease_id, data in self.disease_database.items():
            if crop_type is None or crop_type in data['crops_affected']:
                diseases.append({
                    "disease_id": disease_id,
                    "name": data['name'],
                    "crops_affected": data['crops_affected'],
                    "symptoms": data['symptoms']
                })
        
        return diseases


@lru_cache()
def get_disease_service() -> DiseaseDetectionService:
    """Get singleton instance of disease detection service"""
    return DiseaseDetectionService()
