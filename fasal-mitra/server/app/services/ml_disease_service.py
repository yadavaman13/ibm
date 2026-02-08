"""
ML-Based Disease Detection Service

Integrates TensorFlow/Keras model for real plant disease detection.
"""

import numpy as np
from datetime import datetime
from typing import Optional, Dict, List
import uuid
import logging
import json
import os
from pathlib import Path
from PIL import Image
import io

logger = logging.getLogger(__name__)


class MLDiseaseDetectionService:
    """ML-powered crop disease detection service using TensorFlow"""
    
    def __init__(self):
        """Initialize ML model and disease database"""
        logger.info("[INIT] Initializing ML Disease Detection Service...")
        self.model = None
        self.disease_database = self._load_disease_database()
        logger.info(f"[INIT] Disease database loaded: {len(self.disease_database)} diseases")
        self.class_labels = self._get_class_labels()
        logger.info(f"[INIT] Class labels loaded: {len(self.class_labels)} classes")
        self.model_loaded = False
        
        # Try to load model on initialization
        logger.info("[INIT] Loading TensorFlow model (this may take 30-60 seconds on first load)...")
        try:
            self._load_model()
            logger.info("[INIT] ML Model loaded successfully! Service ready.")
        except Exception as e:
            logger.warning(f"[WARN] Model not loaded on init: {e}. Will use fallback detection.")
    
    def _load_model(self):
        """Load TensorFlow/Keras model"""
        try:
            logger.info("[LOAD] Importing TensorFlow...")
            import tensorflow as tf
            logger.info(f"[LOAD] TensorFlow {tf.__version__} imported successfully")
            
            model_path = Path(__file__).parent.parent / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
            
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Model file not found at {model_path}. "
                    "Please download the model from Google Drive and place it in the correct location. "
                    "See app/models/ml/README.md for instructions."
                )
            
            size_mb = model_path.stat().st_size / (1024 * 1024)
            logger.info(f"[LOAD] Found model file: {model_path.name} ({size_mb:.2f} MB)")
            logger.info(f"[LOAD] Loading model (this takes time, please wait)...")
            
            # Load model without compiling (compile=False) to avoid optimizer compatibility issues
            # We only need the model for inference, not training
            self.model = tf.keras.models.load_model(str(model_path), compile=False)
            self.model_loaded = True
            logger.info("[LOAD] ML model loaded successfully into memory!")
            
        except ImportError as e:
            logger.error(f"TensorFlow not installed: {e}")
            raise ImportError(
                "TensorFlow is required for ML-based disease detection. "
                "Install it with: pip install tensorflow"
            )
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _get_class_labels(self) -> List[str]:
        """Get the list of disease class labels"""
        return [
            'Apple___Apple_scab',
            'Apple___Black_rot',
            'Apple___Cedar_apple_rust',
            'Apple___healthy',
            'Background_without_leaves',
            'Blueberry___healthy',
            'Cherry___Powdery_mildew',
            'Cherry___healthy',
            'Corn___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn___Common_rust',
            'Corn___Northern_Leaf_Blight',
            'Corn___healthy',
            'Grape___Black_rot',
            'Grape___Esca_(Black_Measles)',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)',
            'Peach___Bacterial_spot',
            'Peach___healthy',
            'Pepper,_bell___Bacterial_spot',
            'Pepper,_bell___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Raspberry___healthy',
            'Soybean___healthy',
            'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch',
            'Strawberry___healthy',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]
    
    def _load_disease_database(self) -> Dict:
        """Load disease database from JSON file"""
        try:
            json_path = Path(__file__).parent.parent / "data" / "plant_diseases.json"
            
            if not json_path.exists():
                logger.warning(f"Disease database not found at {json_path}")
                return {}
            
            with open(json_path, 'r', encoding='utf-8') as f:
                diseases = json.load(f)
            
            # Convert list to dictionary keyed by disease name
            return {disease['name']: disease for disease in diseases}
        
        except Exception as e:
            logger.error(f"Error loading disease database: {e}")
            return {}
    
    def _preprocess_image(self, image_data: bytes) -> np.ndarray:
        """
        Preprocess image for model prediction
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Preprocessed numpy array ready for model input
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(image_data))
            logger.info(f"[PREPROCESS] Original image: size={image.size}, mode={image.mode}")
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                logger.info(f"[PREPROCESS] Converted to RGB")
            
            # Resize to model input size (160x160)
            image = image.resize((160, 160))
            logger.info(f"[PREPROCESS] Resized to 160x160")
            
            # Convert to numpy array (uint8 for 0-255 range)
            img_array = np.array(image, dtype=np.float32)
            logger.info(f"[PREPROCESS] Converted to array: shape={img_array.shape}, dtype={img_array.dtype}")
            logger.info(f"[PREPROCESS] Pixel range: min={img_array.min()}, max={img_array.max()}, mean={img_array.mean():.2f}")
            
            # Expand dimensions to match model input shape (1, 160, 160, 3)
            img_array = np.expand_dims(img_array, axis=0)
            
            # NOTE: DO NOT NORMALIZE! Model was trained on 0-255 range
            # (Reference: Plant-Disease-Recognition-System uses img_to_array without normalization)
            logger.info(f"[PREPROCESS] Final array: shape={img_array.shape}, range=[{img_array.min()}, {img_array.max()}]")
            
            return img_array
        
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise ValueError(f"Failed to preprocess image: {e}")
    
    def _get_crop_from_label(self, label: str) -> str:
        """Extract crop name from disease label"""
        if '___' in label:
            return label.split('___')[0].replace(',_bell', '').replace('_', ' ').title()
        return "Unknown"
    
    def _get_severity_from_disease(self, disease_name: str, confidence: float) -> str:
        """Determine severity based on disease type and confidence"""
        # Healthy plants are not severe
        if 'healthy' in disease_name.lower():
            return 'none'
        
        # Background/no plant detected
        if 'background' in disease_name.lower():
            return 'none'
        
        # Severe diseases
        severe_keywords = ['blight', 'rot', 'virus', 'bacterial']
        if any(keyword in disease_name.lower() for keyword in severe_keywords):
            if confidence > 0.85:
                return 'severe'
            elif confidence > 0.70:
                return 'moderate'
            else:
                return 'mild'
        
        # Other fungal diseases
        if confidence > 0.80:
            return 'moderate'
        else:
            return 'mild'
    
    async def detect_disease(
        self,
        image_data: bytes,
        crop_type: str,
        location: Optional[str] = None
    ) -> Dict:
        """
        Detect disease from plant image using ML model
        
        Args:
            image_data: Image file bytes
            crop_type: Type of crop (for filtering/validation)
            location: Optional location information
            
        Returns:
            Dictionary with detection results
        """
        try:
            # Ensure model is loaded
            if not self.model_loaded:
                try:
                    self._load_model()
                except Exception as e:
                    return self._fallback_detection(crop_type, location, str(e))
            
            # Preprocess image
            logger.info(f"[DETECT] Starting disease detection for {crop_type}...")
            processed_image = self._preprocess_image(image_data)
            
            # Make prediction
            import tensorflow as tf
            logger.info(f"[PREDICT] Running model prediction...")
            predictions = self.model.predict(processed_image, verbose=0)
            logger.info(f"[PREDICT] Prediction complete. Shape: {predictions.shape}")
            
            # Log top 5 predictions for debugging
            top_5_indices = np.argsort(predictions[0])[-5:][::-1]
            logger.info(f"[PREDICT] Top 5 predictions:")
            for i, idx in enumerate(top_5_indices, 1):
                logger.info(f"[PREDICT]    {i}. {self.class_labels[idx]}: {predictions[0][idx]*100:.2f}%")
            
            # Get prediction index and confidence
            predicted_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_index])
            
            # Get disease label
            disease_label = self.class_labels[predicted_index]
            logger.info(f"[RESULT] Final prediction: {disease_label} (confidence: {confidence*100:.2f}%)")
            
            # Get disease details from database
            disease_info = self.disease_database.get(disease_label, {
                'name': disease_label,
                'cause': 'Information not available',
                'cure': 'Consult agricultural expert for treatment'
            })
            
            # Extract crop from label
            detected_crop = self._get_crop_from_label(disease_label)
            
            # Determine severity
            severity = self._get_severity_from_disease(disease_label, confidence)
            
            # Check if it's a healthy plant
            is_healthy = 'healthy' in disease_label.lower()
            
            # Prepare response
            response = {
                "detection_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "crop_type": crop_type,
                "detected_crop": detected_crop,
                "location": location,
                "disease_label": disease_label,
                "disease_name": self._format_disease_name(disease_label),
                "is_healthy": is_healthy,
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "cause": disease_info.get('cause', 'Unknown'),
                "treatment": disease_info.get('cure', 'Consult expert'),
                # Farmer-friendly additional information
                "simple_explanation": disease_info.get('simple_explanation', 'Disease information being analyzed. Please consult local expert.'),
                "how_to_spot": disease_info.get('how_to_spot', 'Check with agricultural expert for identification tips.'),
                "prevention_tips": disease_info.get('prevention_tips', 'Follow general good agricultural practices.'),
                "recommendations": self._generate_recommendations(disease_label, severity, confidence, detected_crop),
                "next_steps": self._generate_next_steps(severity, is_healthy),
                "model_used": "TensorFlow CNN (39 classes)"
            }
            
            # Optional: Add LLM-generated personalized advice (if GEMINI_API_KEY is set)
            if not is_healthy and severity != 'none':
                llm_advice = await self.get_llm_treatment_advice(
                    disease_name=self._format_disease_name(disease_label),
                    crop=detected_crop,
                    location=location or "Unknown",
                    severity=severity
                )
                if llm_advice:
                    response['llm_advice'] = llm_advice
                    logger.info("✅ Added LLM-generated treatment advice to response")
            
            return response
        
        except Exception as e:
            logger.error(f"Error in ML disease detection: {str(e)}")
            # Fallback to simulated detection
            return self._fallback_detection(crop_type, location, str(e))
    
    def _format_disease_name(self, label: str) -> str:
        """Format disease label for display"""
        if '___' in label:
            parts = label.split('___')
            crop = parts[0].replace('_', ' ')
            disease = parts[1].replace('_', ' ').replace('(', '(').replace(')', ')')
            return f"{crop} - {disease}".title()
        return label.replace('_', ' ').title()
    
    async def get_llm_treatment_advice(self, disease_name: str, crop: str, location: str, severity: str) -> Optional[str]:
        """
        Get personalized treatment advice from LLM (Gemini API)
        This is an OPTIONAL enhancement for better recommendations
        """
        try:
            import google.generativeai as genai
            import os
            
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                logger.debug("GEMINI_API_KEY not set, skipping LLM advice")
                return None
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""You are an expert agricultural advisor helping farmers.

Disease Detected: {disease_name}
Crop: {crop}
Location: {location}
Severity: {severity}

Provide practical, farmer-friendly advice in simple language with these sections:
1. IMMEDIATE ACTIONS (next 24-48 hours)
2. ORGANIC TREATMENTS (natural, low-cost options)
3. CHEMICAL TREATMENTS (if necessary, with safety warnings)
4. PREVENTION (for future crops)
5. WHEN TO CONSULT EXPERT

IMPORTANT GUIDELINES:
- Use simple language (5th grade reading level)
- Focus on SAFE, affordable, locally-available treatments
- Include safety warnings for chemical treatments
- Suggest consulting local agricultural extension officer for serious cases
- DO NOT recommend specific dosages unless you're certain they're safe
- Prioritize organic/natural solutions first

Keep response concise (under 300 words) and actionable."""
            
            response = model.generate_content(prompt)
            logger.info("✅ LLM advice generated successfully")
            return response.text
            
        except Exception as e:
            logger.warning(f"Could not generate LLM advice: {e}")
            return None
    
    def _generate_recommendations(self, disease_label: str, severity: str, confidence: float, crop: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Healthy plant recommendations
        if 'healthy' in disease_label.lower():
            recommendations.extend([
                f"✅ Your {crop} plant appears healthy!",
                "Continue current care practices",
                "Monitor regularly for any changes",
                "Maintain proper watering and fertilization"
            ])
            return recommendations
        
        # Background/no plant recommendations
        if 'background' in disease_label.lower():
            recommendations.append("⚠️ No plant leaf detected. Please upload a clear image of the affected plant leaf.")
            return recommendations
        
        # Disease detected
        recommendations.append(f"🔍 Disease detected with {confidence:.1f}% confidence")
        
        if severity == 'severe':
            recommendations.extend([
                "⚠️ URGENT: Immediate action required",
                f"Inspect entire {crop} field for similar symptoms",
                "Isolate affected plants immediately",
                "Contact local agricultural extension officer"
            ])
        elif severity == 'moderate':
            recommendations.extend([
                f"⚠️ Monitor your {crop} plants closely",
                "Begin treatment within 24-48 hours",
                "Check neighboring plants for symptoms",
                "Document affected area for tracking"
            ])
        else:  # mild
            recommendations.extend([
                f"Monitor {crop} plants daily",
                "Early intervention can prevent spread",
                "Consider preventive treatment for nearby plants"
            ])
        
        return recommendations
    
    def _generate_next_steps(self, severity: str, is_healthy: bool) -> List[str]:
        """Generate next steps based on severity"""
        if is_healthy:
            return [
                "Continue regular monitoring",
                "Maintain good agricultural practices",
                "Keep records of plant health"
            ]
        
        if severity == 'severe':
            return [
                "1. Apply recommended treatment immediately",
                "2. Remove and destroy severely affected plant parts",
                "3. Prevent spread to healthy plants",
                "4. Consult agricultural expert if condition worsens",
                "5. Monitor daily for the next week"
            ]
        elif severity == 'moderate':
            return [
                "1. Apply recommended treatment within 48 hours",
                "2. Monitor affected plants twice daily",
                "3. Isolate affected area if possible",
                "4. Document progression with photos"
            ]
        else:  # mild or none
            return [
                "1. Apply preventive treatment",
                "2. Monitor daily for changes",
                "3. Maintain good field hygiene",
                "4. Keep records for future reference"
            ]
    
    def _fallback_detection(self, crop_type: str, location: Optional[str], error_msg: str) -> Dict:
        """Fallback detection when ML model is not available"""
        logger.warning(f"Using fallback detection. Reason: {error_msg}")
        
        return {
            "detection_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "crop_type": crop_type,
            "location": location,
            "disease_label": "MODEL_NOT_AVAILABLE",
            "disease_name": "Unable to detect disease",
            "is_healthy": None,
            "confidence": 0.0,
            "severity": "unknown",
            "cause": "ML model not loaded",
            "treatment": "Please ensure the model file is downloaded and placed correctly. See server/app/models/ml/README.md",
            "recommendations": [
                "⚠️ ML model not available. Please contact administrator.",
                "Model file may be missing from server/app/models/ml/",
                "Download model from Google Drive (see README.md)",
                "Fallback: Consult local agricultural expert for manual diagnosis"
            ],
            "next_steps": [
                "1. Download the model file (see documentation)",
                "2. Place it in the correct directory",
                "3. Restart the server",
                "4. For immediate help, consult agricultural expert"
            ],
            "model_used": "Fallback (Model not loaded)",
            "error": error_msg
        }
    
    def get_supported_crops(self) -> List[str]:
        """Get list of crops supported by the model"""
        crops = set()
        for label in self.class_labels:
            if '___' in label:
                crop = label.split('___')[0].replace(',_bell', '').replace('_', ' ').title()
                crops.add(crop)
        return sorted(list(crops))
    
    def get_all_diseases(self, crop_type: Optional[str] = None) -> List[Dict]:
        """Get all known diseases, optionally filtered by crop"""
        diseases = []
        
        for label, info in self.disease_database.items():
            if crop_type:
                detected_crop = self._get_crop_from_label(label)
                if crop_type.lower() not in detected_crop.lower():
                    continue
            
            # Skip healthy and background entries
            if 'healthy' in label.lower() or 'background' in label.lower():
                continue
            
            diseases.append({
                "disease_id": label,
                "name": self._format_disease_name(label),
                "crop": self._get_crop_from_label(label),
                "cause": info.get('cause', 'Unknown'),
                "symptoms": info.get('cure', 'Consult expert')
            })
        
        return diseases


# Singleton instance
_ml_disease_service = None

def get_ml_disease_service() -> MLDiseaseDetectionService:
    """Get singleton instance of ML disease detection service"""
    global _ml_disease_service
    if _ml_disease_service is None:
        logger.info("🔧 Creating ML Disease Detection Service instance...")
        _ml_disease_service = MLDiseaseDetectionService()
        logger.info("🎉 ML Disease Detection Service ready!")
    return _ml_disease_service
