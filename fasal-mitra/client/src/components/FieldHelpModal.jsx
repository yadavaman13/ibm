import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Loader2, AlertCircle, HelpCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import fasalMitraLogo from '../assets/Fasal Mitra logo.png';
import '../styles/field-help-modal.css';

/**
 * FieldHelpModal Component
 * 
 * Modal that displays chatbot interface with auto-filled field-specific question
 * Used for contextual help on agriculture-related input fields
 */
const FieldHelpModal = ({ isOpen, onClose, fieldLabel, fieldName }) => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [error, setError] = useState(null);
    const [sessionId] = useState(() => `field-help-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
    
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const modalRef = useRef(null);

    // Auto-scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Focus input when modal opens
    useEffect(() => {
        if (isOpen && inputRef.current) {
            setTimeout(() => inputRef.current?.focus(), 100);
        }
    }, [isOpen]);

    // Send automatic question when modal opens or field changes
    useEffect(() => {
        if (isOpen && fieldLabel) {
            // Clear previous messages
            setMessages([]);
            setError(null);
            
            // Add welcome message
            const welcomeMessage = {
                id: 'welcome',
                text: `नमस्ते! 🌾 I'll help you understand "${fieldLabel}". Let me explain...`,
                sender: 'bot',
                timestamp: new Date()
            };
            setMessages([welcomeMessage]);
            
            // Auto-send the field explanation request
            sendFieldExplanation(fieldLabel);
        }
    }, [isOpen, fieldLabel]);

    // Handle ESC key to close modal
    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape' && isOpen) {
                onClose();
            }
        };
        
        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        }
        
        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const sendFieldExplanation = async (label) => {
        setIsTyping(true);
        setError(null);

        const cleanLabel = label.replace(/\*/g, '').replace(/\(.*?\)/g, '').trim();
        
        const prompt = `Explain what "${cleanLabel}" means in very simple language for farmers.

Please include:
1. A clear, beginner-friendly explanation (avoid technical jargon)
2. Practical ways a farmer can find or measure this value manually
3. Why this is important for farming
4. Common values or ranges if applicable
5. If possible, suggest YouTube search terms for learning videos

Keep the explanation short, friendly, and focused on practical farming knowledge.`;

        try {
            const response = await fetch('http://localhost:8000/api/v1/chatbot/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: prompt,
                    language: 'en',
                    session_id: sessionId,
                    context: `Field: ${fieldName || label}`
                })
            });

            const data = await response.json();

            if (data.success) {
                const botMessage = {
                    id: `bot-${Date.now()}`,
                    text: data.data.answer,
                    sender: 'bot',
                    timestamp: new Date(),
                    confidence: data.data.confidence
                };
                setMessages(prev => [...prev, botMessage]);
            } else {
                throw new Error(data.message || 'Failed to get explanation');
            }
        } catch (err) {
            console.error('Error getting field explanation:', err);
            setError('Failed to get explanation. Please try again or ask your question manually.');
            
            // Add fallback message
            const fallbackMessage = {
                id: `bot-fallback-${Date.now()}`,
                text: `I apologize, but I'm having trouble connecting to the server right now. 

However, you can ask me anything about "${cleanLabel}" - just type your question below! For example:
- How do I measure this?
- Why is this important?
- What are good values for this?`,
                sender: 'bot',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, fallbackMessage]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleSendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage = {
            id: `user-${Date.now()}`,
            text: inputMessage,
            sender: 'user',
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsTyping(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/v1/chatbot/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: inputMessage,
                    language: 'en',
                    session_id: sessionId,
                    context: `Related to field: ${fieldLabel}`
                })
            });

            const data = await response.json();

            if (data.success) {
                const botMessage = {
                    id: `bot-${Date.now()}`,
                    text: data.data.answer,
                    sender: 'bot',
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, botMessage]);
            } else {
                throw new Error(data.message || 'Failed to get response');
            }
        } catch (err) {
            setError('Failed to get response. Please try again.');
            console.error('Chatbot error:', err);
        } finally {
            setIsTyping(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    // Handle click outside modal to close
    const handleBackdropClick = (e) => {
        if (modalRef.current && !modalRef.current.contains(e.target)) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="field-help-backdrop" onClick={handleBackdropClick}>
            <div className="field-help-modal" ref={modalRef}>
                {/* Header */}
                <div className="field-help-header">
                    <div className="field-help-header-info">
                        <HelpCircle className="w-6 h-6 text-green-600" />
                        <div>
                            <h3 className="field-help-title">Field Help: {fieldLabel}</h3>
                            <p className="field-help-subtitle">AI Assistant Explanation</p>
                        </div>
                    </div>
                    <button 
                        onClick={onClose} 
                        className="field-help-close-btn" 
                        aria-label="Close help"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Messages */}
                <div className="field-help-messages">
                    {messages.map((message) => (
                        <div key={message.id} className={`field-help-message ${message.sender}`}>
                            <div className="field-help-message-content">
                                <div className="field-help-message-text">
                                    {message.sender === 'bot' ? (
                                        <ReactMarkdown>
                                            {message.text}
                                        </ReactMarkdown>
                                    ) : (
                                        <p>{message.text}</p>
                                    )}
                                </div>
                                <span className="field-help-message-time">
                                    {message.timestamp.toLocaleTimeString('en-US', { 
                                        hour: '2-digit', 
                                        minute: '2-digit' 
                                    })}
                                </span>
                            </div>
                        </div>
                    ))}

                    {/* Typing Indicator */}
                    {isTyping && (
                        <div className="field-help-message bot">
                            <div className="field-help-message-content typing-indicator">
                                <div className="typing-dots">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="field-help-error">
                            <AlertCircle className="w-4 h-4" />
                            <span>{error}</span>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="field-help-input-container">
                    <input
                        ref={inputRef}
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask a follow-up question..."
                        className="field-help-input"
                        disabled={isTyping}
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={!inputMessage.trim() || isTyping}
                        className="field-help-send-btn"
                        aria-label="Send message"
                    >
                        {isTyping ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FieldHelpModal;
