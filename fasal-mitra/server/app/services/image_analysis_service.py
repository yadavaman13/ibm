"""
Image Analysis Service for Soil Analysis
Integrates OpenAI Vision API for soil image analysis
"""

import base64
import io
import logging
from typing import Dict, Any, Optional, Union
from functools import lru_cache

from fastapi import UploadFile
from PIL import Image

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("OpenAI package not properly installed. Image analysis features will be limited.")

from app.config import settings

logger = logging.getLogger(__name__)


class ImageAnalysisService:
    """Service for analyzing soil images using OpenAI Vision API"""
    
    def __init__(self):
        """Initialize the image analysis service"""
        self.client = None
        self._initialize_client()
        
        # Soil analysis prompts
        self.soil_analysis_prompt = """
        Analyze this soil image and provide detailed insights about:

        1. **Soil Color**: Describe the soil color and what it indicates about organic matter content and drainage
        2. **Soil Texture**: Assess if the soil appears to be clay, sandy, loamy, or mixed texture
        3. **Moisture Level**: Evaluate the apparent moisture content of the soil
        4. **Organic Matter**: Estimate organic matter content based on soil darkness/color
        5. **Soil Structure**: Comment on soil compaction, aggregation, or any visible issues
        6. **Surface Conditions**: Note any crusting, erosion signs, or surface problems
        7. **Overall Health**: Provide an overall soil health assessment

        Please provide specific, quantitative estimates where possible (e.g., organic matter percentage 2-8%, moisture level dry/moist/wet).
        Format your response as a structured analysis that can be used for agricultural recommendations.
        """
    
    def _initialize_client(self):
        """Initialize OpenAI client with API key"""
        try:
            if not OPENAI_AVAILABLE:
                logger.warning("OpenAI package not available. Image analysis will be limited.")
                return
                
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                logger.warning("OpenAI API key not found in settings. Image analysis will be limited.")
                return
                
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            self.client = None
    
    async def analyze_soil_image(self, image: UploadFile) -> Dict[str, Any]:
        """
        Analyze soil image using OpenAI Vision API
        
        Args:
            image: Uploaded image file
            
        Returns:
            Dictionary containing image analysis results
        """
        try:
            if not self.client:
                logger.warning("OpenAI client not initialized, using fallback analysis")
                return self._fallback_analysis(error="OpenAI client not available")
            
            logger.info(f"Starting OpenAI Vision analysis for image: {image.filename}")
            logger.info(f"API Key available: {bool(settings.OPENAI_API_KEY)}")
            
            # Read and process image
            image_data = await image.read()
            logger.info(f"Image data read, size: {len(image_data)} bytes")
            
            # Reset file pointer for potential re-use
            await image.seek(0)
            
            # Convert to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            logger.info("Image converted to base64 successfully")
            
            # Analyze with OpenAI Vision
            logger.info("Making OpenAI Vision API call...")
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Use the vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.soil_analysis_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            logger.info("OpenAI Vision API call successful")
            logger.info(f"Response received with {len(response.choices)} choices")
            
            # Extract analysis
            analysis_text = response.choices[0].message.content
            logger.info(f"Analysis text received: {analysis_text[:200]}..." if len(analysis_text) > 200 else f"Full analysis: {analysis_text}")
            
            # Parse the analysis into structured data
            structured_analysis = self._parse_analysis_response(analysis_text)
            logger.info(f"Parsed analysis: {structured_analysis}")
            
            return {
                "success": True,
                "analysis_method": "openai_vision",
                "raw_analysis": analysis_text,
                "structured_analysis": structured_analysis,
                "confidence_score": 0.85,  # High confidence for AI analysis
                "analysis_timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Error in OpenAI image analysis: {str(e)}", exc_info=True)
            return self._fallback_analysis(error=str(e))
    
    def _parse_analysis_response(self, analysis_text: str) -> Dict[str, Any]:
        """Parse OpenAI response into structured soil analysis data"""
        
        # Initialize with reasonable defaults
        structured = {
            "soil_color": "medium_brown",
            "texture_type": "loamy",  
            "moisture_level": "moderate",
            "organic_matter_estimate": 4.0,  # 2-8% range
            "compaction_level": "moderate",
            "surface_condition": "good",
            "overall_health_score": 75,  # 0-100 scale
            "visual_indicators": []
        }
        
        if not analysis_text:
            logger.warning("Empty analysis text received from OpenAI")
            return structured
        
        logger.info(f"Parsing analysis text: {analysis_text[:500]}...")
        
        # Extract key information using simple text analysis
        text_lower = analysis_text.lower()
        
        # Soil color analysis with more variations
        if any(word in text_lower for word in ['dark', 'black', 'deep']):
            structured["soil_color"] = "dark_brown"
            structured["organic_matter_estimate"] = 6.0
        elif any(word in text_lower for word in ['light', 'pale', 'yellow', 'tan']):
            structured["soil_color"] = "light_brown"
            structured["organic_matter_estimate"] = 2.5
        elif any(word in text_lower for word in ['red', 'reddish']):
            structured["soil_color"] = "reddish_brown"
        elif any(word in text_lower for word in ['gray', 'grey']):
            structured["soil_color"] = "gray"
            
        # Enhanced texture analysis
        if any(word in text_lower for word in ['clay', 'clayey', 'heavy']):
            structured["texture_type"] = "clay"
        elif any(word in text_lower for word in ['sand', 'sandy', 'gritty']):
            structured["texture_type"] = "sandy"
        elif any(word in text_lower for word in ['loam', 'loamy', 'balanced']):
            structured["texture_type"] = "loamy"
        elif any(word in text_lower for word in ['silt', 'silty', 'smooth']):
            structured["texture_type"] = "silty"
        
        # Enhanced moisture analysis
        if any(word in text_lower for word in ['dry', 'arid', 'parched', 'dusty']):
            structured["moisture_level"] = "low"
        elif any(word in text_lower for word in ['wet', 'moist', 'damp', 'saturated']):
            structured["moisture_level"] = "high"
        elif any(word in text_lower for word in ['moderate', 'medium']):
            structured["moisture_level"] = "moderate"
        
        # Compaction analysis
        if any(word in text_lower for word in ['compact', 'hard', 'dense']):
            structured["compaction_level"] = "high"
        elif any(word in text_lower for word in ['loose', 'crumbly', 'friable']):
            structured["compaction_level"] = "low"
        
        # Health scoring based on multiple indicators
        health_score = 50  # Base score
        
        # Positive indicators
        if any(word in text_lower for word in ['good', 'healthy', 'excellent']):
            health_score += 25
        if any(word in text_lower for word in ['rich', 'fertile', 'nutritious']):
            health_score += 15
        if any(word in text_lower for word in ['organic', 'humus']):
            health_score += 10
            
        # Negative indicators
        if any(word in text_lower for word in ['poor', 'problem', 'issue']):
            health_score -= 20
        if any(word in text_lower for word in ['depleted', 'lacking']):
            health_score -= 15
        if any(word in text_lower for word in ['eroded', 'damaged']):
            health_score -= 10
        
        structured["overall_health_score"] = max(0, min(100, health_score))
        
        # Add visual indicators based on analysis
        indicators = []
        if structured["soil_color"] == "dark_brown":
            indicators.append("Rich organic matter content indicated by dark color")
        if structured["texture_type"] == "loamy":
            indicators.append("Balanced texture good for most crops")
        if structured["moisture_level"] == "high":
            indicators.append("Good moisture retention observed")
            
        structured["visual_indicators"] = indicators or ["General soil analysis completed"]
        
        logger.info(f"Parsed structured analysis: {structured}")
        return structured
    
    def _fallback_analysis(self, error: Optional[str] = None) -> Dict[str, Any]:
        """Provide fallback analysis when OpenAI is not available"""
        return {
            "success": False,
            "analysis_method": "fallback",
            "error": error,
            "structured_analysis": {
                "soil_color": "N/A",
                "texture_type": "N/A", 
                "moisture_level": "N/A",
                "organic_matter_estimate": 3.0,  # Average estimate
                "compaction_level": "N/A",
                "surface_condition": "N/A",
                "overall_health_score": 50,  # Neutral score
                "visual_indicators": ["Visual analysis unavailable - please ensure a soil image is uploaded for AI analysis"]
            },
            "message": "Image analysis not available. Using traditional soil testing data only.",
            "analysis_timestamp": self._get_timestamp()
        }
    
    async def combine_analyses(
        self,
        image_analysis: Dict[str, Any],
        traditional_analysis: Dict[str, Any],
        state: str,
        crop: str
    ) -> Dict[str, Any]:
        """
        Combine image analysis with traditional soil analysis
        
        Args:
            image_analysis: Results from image analysis
            traditional_analysis: Results from traditional soil testing
            state: State name
            crop: Target crop
            
        Returns:
            Combined analysis with enhanced recommendations
        """
        try:
            combined = {
                "analysis_type": "hybrid_analysis",
                "confidence": "high" if image_analysis.get("success", False) else "medium",
                "state": state,
                "crop": crop,
                "timestamp": self._get_timestamp()
            }
            
            # Combine soil health indicators
            image_struct = image_analysis.get("structured_analysis", {})
            traditional_data = traditional_analysis.get("basic_suitability", {})
            
            # Enhanced soil assessment
            combined["soil_assessment"] = {
                "visual_health_score": image_struct.get("overall_health_score", 50),
                "chemical_suitability_score": traditional_data.get("suitability_score", 50),
                "texture_analysis": {
                    "visual_texture": image_struct.get("texture_type", "unknown"),
                    "moisture_level": image_struct.get("moisture_level", "unknown"),
                    "compaction_status": image_struct.get("compaction_level", "unknown")
                },
                "organic_matter": {
                    "visual_estimate": image_struct.get("organic_matter_estimate", 3.0),
                    "color_indicators": image_struct.get("soil_color", "unknown")
                }
            }
            
            # Enhanced recommendations
            combined["enhanced_recommendations"] = self._generate_hybrid_recommendations(
                image_analysis, traditional_analysis, crop
            )
            
            # Risk assessment
            combined["risk_factors"] = self._assess_combined_risks(
                image_analysis, traditional_analysis
            )
            
            # Action items
            combined["priority_actions"] = self._generate_priority_actions(
                image_analysis, traditional_analysis
            )
            
            return combined
            
        except Exception as e:
            logger.error(f"Error combining analyses: {str(e)}")
            return {
                "analysis_type": "hybrid_analysis", 
                "error": str(e),
                "fallback_message": "Using traditional analysis only"
            }
    
    def _generate_hybrid_recommendations(
        self,
        image_analysis: Dict[str, Any],
        traditional_analysis: Dict[str, Any],
        crop: str
    ) -> list[str]:
        """Generate recommendations combining both analyses"""
        recommendations = []
        
        # Get image insights
        image_struct = image_analysis.get("structured_analysis", {})
        
        # Visual-based recommendations
        if image_struct.get("moisture_level") == "low":
            recommendations.append("🚿 Visual analysis indicates dry soil - increase irrigation frequency")
        
        if image_struct.get("organic_matter_estimate", 3) < 3:
            recommendations.append("🌱 Soil appears low in organic matter - add compost or organic fertilizers")
        
        if image_struct.get("compaction_level") == "high":
            recommendations.append("🔧 Soil shows signs of compaction - consider deep tillage or subsoiling")
        
        # Combine with traditional recommendations
        traditional_recs = traditional_analysis.get("recommendations", [])
        recommendations.extend(traditional_recs[:3])  # Top 3 traditional recommendations
        
        return recommendations[:6]  # Return top 6 combined recommendations
    
    def _assess_combined_risks(
        self,
        image_analysis: Dict[str, Any],
        traditional_analysis: Dict[str, Any]
    ) -> list[str]:
        """Assess risks from combined analysis"""
        risks = []
        
        image_struct = image_analysis.get("structured_analysis", {})
        
        # Visual risk indicators
        if image_struct.get("overall_health_score", 50) < 40:
            risks.append("⚠️ Visual soil health appears poor")
        
        if image_struct.get("compaction_level") == "high":
            risks.append("🚨 Soil compaction may limit root growth")
        
        if image_struct.get("moisture_level") == "low":
            risks.append("💧 Low soil moisture may stress plants")
        
        # Chemical risks from traditional analysis
        basic_analysis = traditional_analysis.get("basic_suitability", {})
        if not basic_analysis.get("suitable", True):
            risks.append("⚗️ Chemical analysis shows nutrient imbalances")
        
        return risks[:4]  # Top 4 risks
    
    def _generate_priority_actions(
        self,
        image_analysis: Dict[str, Any],
        traditional_analysis: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """Generate prioritized action items"""
        actions = []
        
        # High priority actions based on image analysis
        image_struct = image_analysis.get("structured_analysis", {})
        
        if image_struct.get("compaction_level") == "high":
            actions.append({
                "priority": "high",
                "action": "Address soil compaction",
                "method": "Deep tillage or subsoiling",
                "timing": "Before next planting season"
            })
        
        if image_struct.get("organic_matter_estimate", 3) < 2:
            actions.append({
                "priority": "medium",
                "action": "Increase organic matter",
                "method": "Add 2-3 tons compost per hectare",
                "timing": "Before crop planting"
            })
        
        # Add traditional analysis priorities
        if not traditional_analysis.get("basic_suitability", {}).get("suitable", True):
            actions.append({
                "priority": "high",
                "action": "Correct nutrient deficiencies",
                "method": "Apply targeted fertilizers as per soil test",
                "timing": "Immediate"
            })
        
        return actions[:3]  # Top 3 priority actions
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis"""
        from datetime import datetime
        return datetime.now().isoformat()


@lru_cache()
def get_image_service() -> ImageAnalysisService:
    """Get singleton instance of image analysis service"""
    return ImageAnalysisService()