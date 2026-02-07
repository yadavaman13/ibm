import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, Loader2, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import fasalMitraLogo from '../assets/Fasal Mitra logo.png';
import '../styles/chatbot-widget.css';

const ChatbotWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [error, setError] = useState(null);
    const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
    
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Welcome message on first open
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([
                {
                    id: 'welcome',
                    text: 'नमस्ते! 🌾 Welcome to FasalMitra! I\'m your AI farming assistant. Ask me anything about crops, diseases, weather, or farming techniques.',
                    sender: 'bot',
                    timestamp: new Date()
                }
            ]);
        }
    }, [isOpen, messages.length]);

    // Auto-scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Focus input when opened
    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const toggleChat = () => {
        setIsOpen(!isOpen);
        setError(null);
    };

    const detectLanguage = (text) => {
        // Simple language detection based on character sets
        const hindiPattern = /[\u0900-\u097F]/; // Devanagari script
        const tamilPattern = /[\u0B80-\u0BFF]/; // Tamil script
        const teluguPattern = /[\u0C00-\u0C7F]/; // Telugu script
        
        if (hindiPattern.test(text)) return 'hi';
        if (tamilPattern.test(text)) return 'ta';
        if (teluguPattern.test(text)) return 'te';
        return 'en';
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
        const detectedLanguage = detectLanguage(inputMessage);
        setInputMessage('');
        setIsTyping(true);
        setError(null);

        try {
            const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            console.log('🤖 Chatbot - Using API URL:', baseUrl);
            const response = await fetch(`${baseUrl}/api/v1/chatbot/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: inputMessage,
                    language: detectedLanguage,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                console.error('Chatbot API error:', response.status, data);
                throw new Error(`Server error: ${response.status} - ${data.detail || data.message || 'Unknown error'}`);
            }

            if (data.success) {
                const botMessage = {
                    id: `bot-${Date.now()}`,
                    text: data.data.answer,
                    sender: 'bot',
                    timestamp: new Date(),
                    confidence: data.data.confidence,
                    relatedTopics: data.data.related_topics
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

    const handleEscapeKey = (e) => {
        if (e.key === 'Escape' && isOpen) {
            setIsOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener('keydown', handleEscapeKey);
        return () => document.removeEventListener('keydown', handleEscapeKey);
    }, [isOpen]);

    return (
        <div className="chatbot-widget">
            {/* Chat Window */}
            {isOpen && (
                <div className="chatbot-window">
                    {/* Header */}
                    <div className="chatbot-header">
                        <div className="chatbot-header-info">
                            <img src={fasalMitraLogo} alt="FasalMitra" className="chatbot-logo" />
                            <div>
                                <h3 className="chatbot-title">FasalMitra AI</h3>
                                <p className="chatbot-status">
                                    <span className="status-dot"></span>
                                    Online
                                </p>
                            </div>
                        </div>
                        <button onClick={toggleChat} className="chatbot-close-btn" aria-label="Close chat">
                            <X className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="chatbot-messages">
                        {messages.map((message) => (
                            <div key={message.id} className={`message ${message.sender}`}>
                                <div className="message-content">
                                    <div className="message-text">
                                        {message.sender === 'bot' ? (
                                            <ReactMarkdown>
                                                {message.text}
                                            </ReactMarkdown>
                                        ) : (
                                            <p>{message.text}</p>
                                        )}
                                    </div>
                                    <span className="message-time">
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
                            <div className="message bot">
                                <div className="message-content typing-indicator">
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
                            <div className="chatbot-error">
                                <AlertCircle className="w-4 h-4" />
                                <span>{error}</span>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="chatbot-input-container">
                        <input
                            ref={inputRef}
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask about crops, diseases, weather..."
                            className="chatbot-input"
                            disabled={isTyping}
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={!inputMessage.trim() || isTyping}
                            className="chatbot-send-btn"
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
            )}

            {/* Floating Button */}
            <button
                onClick={toggleChat}
                className={`chatbot-toggle-btn ${isOpen ? 'open' : ''}`}
                aria-label="Toggle chat"
            >
                {isOpen ? (
                    <X className="w-6 h-6" />
                ) : (
                    <img src={fasalMitraLogo} alt="Chat" className="toggle-logo" />
                )}
            </button>
        </div>
    );
};

export default ChatbotWidget;
