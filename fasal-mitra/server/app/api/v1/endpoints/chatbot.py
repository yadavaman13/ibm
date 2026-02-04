"""
Chatbot API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from app.models.chatbot import (
    ChatbotQueryRequest,
    ChatbotResponse,
    ExplainTermRequest,
    ExplainTermResponse,
    ConversationHistory
)
from app.models.common import ResponseModel
from app.services.chatbot_service import ChatbotService, get_chatbot_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=ResponseModel)
async def ask_question(
    request: ChatbotQueryRequest,
    service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Ask a farming-related question to the AI chatbot
    
    - **question**: The question to ask (3-500 characters)
    - **context**: Optional additional context
    - **language**: Response language code (default: "en")
    - **session_id**: Optional session ID for conversation tracking
    
    Returns AI-generated answer with related topics and sources
    """
    try:
        result = await service.ask_question(request)
        
        return ResponseModel(
            success=True,
            message="Question answered",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in chatbot query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=ResponseModel)
async def explain_term(
    request: ExplainTermRequest,
    service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Explain a farming/agricultural term
    
    - **term**: The term to explain (2-100 characters)
    - **language**: Response language (default: "en")
    - **context**: Optional context where the term appears
    
    Returns detailed explanation with examples and related terms
    """
    try:
        result = await service.explain_term(request)
        
        return ResponseModel(
            success=True,
            message=f"Term '{request.term}' explained",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error explaining term: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{session_id}", response_model=ResponseModel)
async def get_conversation(
    session_id: str,
    service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Get conversation history for a session
    
    - **session_id**: Session identifier
    
    Returns conversation history (will be implemented with database)
    """
    return ResponseModel(
        success=True,
        message="Conversation history",
        data={
            "session_id": session_id,
            "messages": [],
            "note": "Conversation tracking will be implemented with database integration"
        }
    )


@router.get("/status", response_model=ResponseModel)
async def get_chatbot_status(service: ChatbotService = Depends(get_chatbot_service)):
    """Get chatbot service status"""
    status = service.get_status()
    
    return ResponseModel(
        success=True,
        message="Chatbot status",
        data=status
    )
