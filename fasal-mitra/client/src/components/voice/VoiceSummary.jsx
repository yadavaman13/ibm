import React, { useState, useEffect, useMemo } from 'react';
import { AlertTriangle, Volume2 } from 'lucide-react';
import SpeechControls from './SpeechControls';
import VoiceLanguageSelector from './VoiceLanguageSelector';
import resultSummaryGenerator from '../../utils/resultSummaryGenerator';
import voiceService from '../../services/voiceService';
import './VoiceSummary.css';

const VoiceSummary = ({ 
    result,
    resultType,
    title = "Audio Summary",
    showTitle = true,
    autoPlay = false,
    compact = false,
    className = '',
    onSpeechStart = () => {},
    onSpeechEnd = () => {},
    onSpeechError = () => {}
}) => {
    const [selectedLanguage, setSelectedLanguage] = useState('en');
    const [isExpanded, setIsExpanded] = useState(!compact);
    const [voiceAvailable, setVoiceAvailable] = useState(true);
    const [showFullPreview, setShowFullPreview] = useState(false);

    // Check if native voice is available for selected language
    useEffect(() => {
        const checkVoice = () => {
            const hasVoice = voiceService.hasNativeVoice(selectedLanguage);
            setVoiceAvailable(hasVoice);
            console.log(`Voice check for ${selectedLanguage}: ${hasVoice ? 'available' : 'not available'}`);
        };
        
        // Check after a small delay to ensure voices are loaded
        const timer = setTimeout(checkVoice, 100);
        return () => clearTimeout(timer);
    }, [selectedLanguage]);

    // Determine the actual language to use for text generation
    // If no voice available for selected language, use English
    const effectiveLanguage = useMemo(() => {
        if (selectedLanguage === 'en') return 'en';
        return voiceAvailable ? selectedLanguage : 'en';
    }, [selectedLanguage, voiceAvailable]);

    // Generate speech text based on result and EFFECTIVE language
    const speechText = useMemo(() => {
        if (!result || !resultType) return '';
        
        try {
            return resultSummaryGenerator.generateSummary(result, resultType, effectiveLanguage);
        } catch (error) {
            console.error('Error generating speech summary:', error);
            return 'Summary not available.';
        }
    }, [result, resultType, effectiveLanguage]);

    // Clean speech text for better synthesis
    const cleanSpeechText = useMemo(() => {
        return resultSummaryGenerator.cleanTextForSpeech(speechText);
    }, [speechText]);

    const handleLanguageChange = (language) => {
        setSelectedLanguage(language);
    };

    const toggleExpanded = () => {
        setIsExpanded(!isExpanded);
    };

    // Don't render if no result
    if (!result) {
        return null;
    }

    return (
        <div className={`voice-summary ${compact ? 'compact' : ''} ${className}`}>
            {/* Header */}
            {showTitle && (
                <div className="voice-summary-header" onClick={compact ? toggleExpanded : undefined}>
                    <div className="header-content">
                        <h3 className="header-title">{title}</h3>
                    </div>
                    <div className="header-status">
                        <Volume2 className="status-icon" />
                        <span className="status-text">Ready</span>
                    </div>
                    {compact && (
                        <button 
                            className="expand-button"
                            onClick={toggleExpanded}
                            aria-label={isExpanded ? "Collapse audio summary" : "Expand audio summary"}
                        >
                            {isExpanded ? '−' : '+'}
                        </button>
                    )}
                </div>
            )}

            {/* Content */}
            {(!compact || isExpanded) && (
                <div className="voice-summary-content">
                    {/* Left side - Controls */}
                    <div className="voice-controls-group">
                        {/* Language Selection */}
                        <VoiceLanguageSelector
                            selectedLanguage={selectedLanguage}
                            onLanguageChange={handleLanguageChange}
                            compact={compact}
                            showLabel={false}
                        />

                        {/* Speech Controls */}
                        <SpeechControls
                            text={cleanSpeechText}
                            language={effectiveLanguage}
                            resultType={resultType}
                            autoPlay={autoPlay}
                            showSettings={!compact}
                            className={compact ? 'compact' : ''}
                            onStart={onSpeechStart}
                            onEnd={onSpeechEnd}
                            onError={onSpeechError}
                        />
                    </div>

                    {/* Right side - Summary Preview */}
                    {!compact && speechText && (
                        <div className="summary-preview">
                            <div className="preview-header">
                                <span>Summary Preview</span>
                            </div>
                            <div className="preview-content">
                                <p className={`preview-text ${showFullPreview ? 'expanded' : ''}`}>
                                    {showFullPreview 
                                        ? speechText
                                        : (speechText.length > 200 
                                            ? speechText.substring(0, 200) + '...'
                                            : speechText)
                                    }
                                </p>
                                {speechText.length > 200 && (
                                    <button 
                                        className="show-more-btn"
                                        onClick={() => setShowFullPreview(!showFullPreview)}
                                    >
                                        {showFullPreview ? 'Show less' : 'Show more'}
                                    </button>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default VoiceSummary;