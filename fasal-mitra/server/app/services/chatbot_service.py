"""
Chatbot Service

AI-powered farming assistant using Google Gemini API
"""

import os
from typing import Optional, Dict, List
import logging
from functools import lru_cache
from datetime import datetime
import uuid
import time

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Chatbot will use fallback mode.")

from app.config import settings
from app.models.chatbot import (
    ChatbotQueryRequest,
    ExplainTermRequest
)

logger = logging.getLogger(__name__)


class ChatbotService:
    """AI-powered farming chatbot service"""
    
    def __init__(self):
        self.enabled = False
        self.model = None
        self.last_request_time = None
        self.min_request_interval = 2  # seconds between requests
        
        # Initialize Gemini if available
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.enabled = True
                logger.info("✅ Gemini API configured successfully")
            except Exception as e:
                logger.error(f"Error configuring Gemini API: {str(e)}")
                self.enabled = False
        else:
            logger.warning("Chatbot disabled - Gemini API key not configured")
    
    async def ask_question(self, request: ChatbotQueryRequest) -> Dict:
        """Answer a farming question"""
        
        if not self.enabled:
            return self._fallback_response(request.question)
        
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Create context-aware prompt
            prompt = self._create_question_prompt(request)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            result = {
                "response_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "question": request.question,
                "answer": response.text,
                "language": request.language,
                "confidence": 0.85,
                "related_topics": self._extract_related_topics(response.text),
                "sources": ["AI-Generated", "Agricultural Knowledge Base"],
                "session_id": request.session_id
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Error in chatbot query: {str(e)}")
            return self._fallback_response(request.question)
    
    async def explain_term(self, request: ExplainTermRequest) -> Dict:
        """Explain a farming term"""
        
        if not self.enabled:
            return self._fallback_term_explanation(request.term)
        
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Create explanation prompt
            prompt = self._create_explanation_prompt(request)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            result = {
                "term": request.term,
                "explanation": response.text,
                "examples": self._extract_examples(response.text),
                "related_terms": self._extract_related_terms(request.term),
                "language": request.language,
                "measurement_method": None,
                "learning_resources": [
                    "Local agricultural extension office",
                    "Agricultural universities",
                    "Online farming courses"
                ]
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Error explaining term: {str(e)}")
            return self._fallback_term_explanation(request.term)
    
    def get_status(self) -> Dict:
        """Get chatbot service status"""
        return {
            "enabled": self.enabled,
            "gemini_available": GEMINI_AVAILABLE,
            "api_key_configured": bool(settings.GEMINI_API_KEY),
            "model": "gemini-2.0-flash-exp" if self.enabled else None,
            "status": "operational" if self.enabled else "fallback_mode"
        }
    
    def _create_question_prompt(self, request: ChatbotQueryRequest) -> str:
        """Create context-aware prompt for questions"""
        prompt = f"""You are an expert agricultural advisor helping Indian farmers. 
        
Question: {request.question}

Context: {request.context or 'General farming inquiry'}

Please provide a helpful, practical answer that:
1. Is specific to Indian farming conditions
2. Uses simple language that farmers can understand
3. Includes actionable advice
4. Mentions approximate costs in INR if relevant
5. Considers local climate and soil conditions

Answer in {request.language} language if not English.
"""
        return prompt
    
    def _create_explanation_prompt(self, request: ExplainTermRequest) -> str:
        """Create prompt for term explanation"""
        prompt = f"""Explain the agricultural term "{request.term}" in a way that farmers can understand.

Include:
1. Simple definition
2. Why it matters for farming
3. How to measure or identify it
4. Practical examples
5. Related terms

Context: {request.context or 'General farming context'}

Explain in {request.language} language if not English.
Keep it practical and farmer-friendly.
"""
        return prompt
    
    def _wait_for_rate_limit(self):
        """Implement rate limiting"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        
        self.last_request_time = time.time()
    
    def _extract_related_topics(self, text: str) -> List[str]:
        """Extract related topics from response (simple implementation)"""
        # In production, use NLP to extract topics
        keywords = ["fertilizer", "irrigation", "pesticide", "soil", "weather", "crop rotation"]
        found_topics = [kw for kw in keywords if kw.lower() in text.lower()]
        return found_topics[:3]
    
    def _extract_examples(self, text: str) -> List[str]:
        """Extract examples from text"""
        # Simple extraction - in production, use better NLP
        return ["See explanation above for practical examples"]
    
    def _extract_related_terms(self, term: str) -> List[str]:
        """Get related terms"""
        # Predefined related terms
        related_map = {
            'pH': ['soil acidity', 'lime application', 'sulfur treatment'],
            'NPK': ['nitrogen', 'phosphorus', 'potassium', 'fertilizer'],
            'irrigation': ['water management', 'drip irrigation', 'sprinkler'],
            'yield': ['productivity', 'harvest', 'crop output']
        }
        
        for key, related in related_map.items():
            if key.lower() in term.lower():
                return related
        
        return []
    
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when Gemini is not available"""
        return {
            "response_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "question": question,
            "answer": """Thank you for your question about farming. 
            
The AI chatbot is currently unavailable. Please:
1. Contact your local agricultural extension office
2. Consult with experienced farmers in your area
3. Check government agricultural websites for guidance
4. Use other features of FasalMitra for crop and yield predictions

For immediate assistance, please enable the Gemini API by setting GEMINI_API_KEY in your environment variables.""",
            "language": "en",
            "confidence": 0.5,
            "related_topics": [],
            "sources": ["System Message"],
            "session_id": None
        }
    
    def _fallback_term_explanation(self, term: str) -> Dict:
        """Fallback term explanation"""
        common_terms = {
            'pH': 'A measure of soil acidity or alkalinity. Range: 0-14, with 7 being neutral. Most crops prefer pH 6-7.',
            'NPK': 'The three main nutrients in fertilizer: Nitrogen (N), Phosphorus (P), and Potassium (K).',
            'yield': 'The amount of crop produced per unit area, usually measured in tons per hectare.',
            'irrigation': 'The artificial application of water to crops to help growth.',
            'fertilizer': 'Substance added to soil to supply nutrients for plant growth.'
        }
        
        explanation = common_terms.get(
            term.lower(), 
            f"'{term}' is an agricultural term. Please consult agricultural resources for detailed information."
        )
        
        return {
            "term": term,
            "explanation": explanation,
            "examples": ["Contact local agricultural experts for examples"],
            "related_terms": [],
            "language": "en",
            "measurement_method": "Consult agricultural extension services",
            "learning_resources": ["Local agricultural office", "Agricultural websites"]
        }


@lru_cache()
def get_chatbot_service() -> ChatbotService:
    """Get singleton instance of chatbot service"""
    return ChatbotService()
