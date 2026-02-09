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
                # Using Gemini Flash Latest (best balance of speed and quota)
                self.model = genai.GenerativeModel('gemini-flash-latest')
                self.enabled = True
                logger.info("✅ Gemini API configured successfully with gemini-flash-latest")
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
            "model": "gemini-flash-latest" if self.enabled else None,
            "status": "operational" if self.enabled else "fallback_mode"
        }
    
    def _create_question_prompt(self, request: ChatbotQueryRequest) -> str:
        """Create context-aware prompt for questions"""
        
        # Language-specific instructions
        language_map = {
            'hi': 'Hindi (हिंदी)',
            'en': 'English',
            'ta': 'Tamil (தமிழ்)',
            'te': 'Telugu (తెలుగు)',
            'mr': 'Marathi (मराठी)',
            'bn': 'Bengali (বাংলা)',
            'gu': 'Gujarati (ગુજરાતી)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'ml': 'Malayalam (മലയാളം)',
            'pa': 'Punjabi (ਪੰਜਾਬੀ)'
        }
        
        language_name = language_map.get(request.language, 'English')
        
        prompt = f"""You are FasalMitra AI - an expert agricultural advisor for Indian farmers.

LANGUAGE: Respond in {language_name}

USER QUESTION: {request.question}

CONTEXT: {request.context or 'General farming inquiry'}

CRITICAL RESPONSE GUIDELINES:
1. **BE CONCISE**: Keep responses SHORT (max 150 words) and focused on KEY POINTS only
2. **STRUCTURE WELL**: Use this format:
   - Start with a brief direct answer (1-2 sentences)
   - Key Points: Use bullet points (•) with emojis for visual clarity
   - Add practical tips if space allows
   - End with YouTube search hint if relevant (e.g., "🎥 Search: 'organic farming Hindi tutorial'")

3. **HANDLE ALL QUESTIONS**:
   - Farming questions: Give specific, actionable advice
   - Non-farming questions: Politely redirect to farming topics
   - Unclear questions: Ask for clarification
   - Greetings: Respond warmly and ask how you can help

4. **MAKE IT PRACTICAL**:
   - Mention costs in ₹ if relevant
   - Use simple words farmers understand
   - Focus on Indian farming conditions
   - Include seasonal advice when applicable

5. **YOUTUBE INTEGRATION**:
   - For "how-to" questions, add: "🎥 Watch: 'topic language tutorial'" at the end
   - Suggest specific search terms in user's language
   - Example: "🎥 Search YouTube: 'टमाटर की खेती हिंदी में'"

EXAMPLE GOOD RESPONSE:
Question: "How to grow tomatoes?"

Tomatoes grow best in well-drained soil with plenty of sunlight.

**Key Steps:**
• 🌱 Seeds: Start indoors 6-8 weeks before planting
• 🌞 Location: Full sun (6-8 hours daily)
• 💧 Water: Regular but not excessive
• 🌿 Support: Use stakes or cages (₹50-100)

**Quick Tip:** Add compost before planting for better yield.

🎥 Search YouTube: "tomato farming in India" for video tutorials.

Remember: CONCISE, STRUCTURED, PRACTICAL. Always stay helpful and friendly!
"""
        return prompt
    
    def _create_explanation_prompt(self, request: ExplainTermRequest) -> str:
        """Create prompt for term explanation"""
        prompt = f"""Explain the agricultural term "{request.term}" in simple language for farmers.

KEEP IT SHORT (max 100 words) and STRUCTURED:

**Definition:** One clear sentence

**Why It Matters:** How it affects farming (1-2 sentences)

**How to Measure/Identify:** Practical method

**Example:** One real-world example

**Related Terms:** 2-3 similar concepts

Add this if helpful:
🎥 For detailed tutorial, search YouTube: "{request.term} farming explanation"

Context: {request.context or 'General farming context'}

Language: {request.language}
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
