import React, { useState, useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { X, Send, Loader2, AlertCircle, HelpCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import fasalMitraLogo from '../assets/Fasal Mitra logo.png';
import useVoiceRecognition from '../hooks/useVoiceRecognition';
import useTextToSpeech from '../hooks/useTextToSpeech';
import VoiceInputButton from './VoiceInputButton';
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
    const [voiceLanguage, setVoiceLanguage] = useState('en-IN');
    const [isRecording, setIsRecording] = useState(false);
    
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const modalRef = useRef(null);
    const lastBotMessageRef = useRef(null);
    const lastTranscriptRef = useRef('');
    const sendMessageToAPIRef = useRef(null);

    // Separate API function to avoid circular dependencies in callbacks
    const sendMessageToAPI = useCallback(async (messageText) => {
        if (!messageText.trim()) return;

        setIsTyping(true);
        setError(null);

        try {
            const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
            const response = await fetch(`${baseUrl}/api/v1/chatbot/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: messageText,
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
                lastBotMessageRef.current = botMessage.text;
            } else {
                throw new Error(data.message || 'Failed to get response');
            }
        } catch (err) {
            setError('Failed to get response. Please try again.');
            console.error('Chatbot error:', err);
        } finally {
            setIsTyping(false);
        }
    }, [sessionId, fieldLabel]);

    // Store API function in ref for stable access
    useEffect(() => {
        sendMessageToAPIRef.current = sendMessageToAPI;
    }, [sendMessageToAPI]);

    // Stable callbacks for voice recognition
    const handleVoiceResult = useCallback((transcript) => {
        console.log('📝 Final voice result received:', transcript);
        lastTranscriptRef.current = transcript;
        // Send the message immediately when final result is received
        if (transcript.trim()) {
            const userMessage = {
                id: `user-${Date.now()}`,
                text: transcript,
                sender: 'user',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, userMessage]);
            sendMessageToAPIRef.current?.(transcript);
        }
    }, []);

    const handleVoiceError = useCallback((errorMessage) => {
        console.error('🎤 Voice error:', errorMessage);
        setError(errorMessage);
        // Auto-clear error after 3 seconds
        setTimeout(() => {
            setError(null);
        }, 3000);
    }, []);

    // Voice Recognition Hook
    const {
        isListening,
        isSupported: isVoiceSupported,
        transcript: liveTranscript,
        startListening,
        stopListening
    } = useVoiceRecognition({
        language: voiceLanguage,
        onResult: handleVoiceResult,
        onError: handleVoiceError
    });

    // Sync recording state with actual speech recognition
    useEffect(() => {
        if (!isListening && isRecording) {
            setIsRecording(false);
        }
    }, [isListening, isRecording]);

    // Text-to-Speech Hook
    const {
        speak,
        stop: stopSpeaking,
        isSpeaking
    } = useTextToSpeech({
        language: voiceLanguage,
        rate: 1.0,
        pitch: 1.0,
        volume: 1.0
    });

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
            const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
            const response = await fetch(`${baseUrl}/api/v1/chatbot/query`, {
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

    const handleSendMessage = async (textToSend = null) => {
        const messageText = textToSend || inputMessage;
        if (!messageText.trim()) return;
        
        setInputMessage('');
        await sendMessageToAPI(messageText);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const handleVoiceInput = () => {
        setError(null); // Clear any previous errors
        setInputMessage(''); // Clear input field when starting to listen
        setIsRecording(true); // Set local recording state
        startListening();
    };

    const handleStopVoiceInput = () => {
        setIsRecording(false); // Immediately clear local recording state
        stopListening();
        // Message will be sent via handleVoiceResult when final transcript arrives
    };

    // Handle click outside modal to close
    const handleBackdropClick = (e) => {
        if (modalRef.current && !modalRef.current.contains(e.target)) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return createPortal(
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
                    <div className="field-help-input-wrapper">
                        {/* Voice Input Button */}
                        <VoiceInputButton
                            isListening={isRecording}
                            isSupported={isVoiceSupported}
                            onStartListening={handleVoiceInput}
                            onStopListening={handleStopVoiceInput}
                            disabled={isTyping}
                        />

                        {/* Text Input with Recording/Processing Indicator */}
                        <div className="input-with-indicator">
                            <input
                                ref={inputRef}
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder={isRecording ? "Listening..." : "Ask a follow-up question..."}
                                className={`field-help-input ${isRecording ? 'recording' : ''}`}
                                disabled={isTyping}
                                readOnly={isRecording}
                            />
                            {isRecording && (
                                <div className="recording-indicator">
                                    <span className="recording-dot"></span>
                                    <span className="recording-text">Recording</span>
                                    <span className="recording-wave">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </span>
                                </div>
                            )}
                        </div>

                        {/* Send Button */}
                        <button
                            onClick={() => handleSendMessage()}
                            disabled={!inputMessage.trim() || isTyping || isRecording}
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
        </div>,
        document.body
    );
};

export default FieldHelpModal;
