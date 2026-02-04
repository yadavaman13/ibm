"""
Pydantic models for Chatbot API
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    """Types of chatbot queries"""
    GENERAL = "general"
    TECHNICAL = "technical"
    DISEASE = "disease"
    CROP_ADVICE = "crop_advice"
    WEATHER = "weather"
    PRICING = "pricing"


class ChatbotQueryRequest(BaseModel):
    """Request model for chatbot query"""
    question: str = Field(..., min_length=3, max_length=500, description="Farmer's question")
    context: Optional[str] = Field(None, description="Additional context")
    language: str = Field(default="en", description="Response language code (en, hi, etc.)")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")


class ChatbotResponse(BaseModel):
    """Response model for chatbot"""
    response_id: str
    timestamp: datetime
    question: str
    answer: str
    language: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    related_topics: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    session_id: Optional[str] = None


class ExplainTermRequest(BaseModel):
    """Request to explain a farming term"""
    term: str = Field(..., min_length=2, max_length=100, description="Farming term to explain")
    language: str = Field(default="en", description="Response language")
    context: Optional[str] = Field(None, description="Context where term appears")


class ExplainTermResponse(BaseModel):
    """Response for term explanation"""
    term: str
    explanation: str
    examples: List[str]
    related_terms: List[str]
    language: str
    measurement_method: Optional[str] = None
    learning_resources: List[str] = Field(default_factory=list)


class ConversationMessage(BaseModel):
    """Single message in conversation"""
    role: str = Field(..., description="user or assistant")
    content: str
    timestamp: datetime


class ConversationHistory(BaseModel):
    """Conversation history"""
    session_id: str
    messages: List[ConversationMessage]
    created_at: datetime
    last_updated: datetime
