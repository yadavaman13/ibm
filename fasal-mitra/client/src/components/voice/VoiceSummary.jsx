import React, { useState, useEffect, useMemo } from 'react';
import { Volume2, MessageSquare } from 'lucide-react';
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

    // Generate speech text based on result and language
    const speechText = useMemo(() => {
        if (!result || !resultType) return '';
        
        try {
            return resultSummaryGenerator.generateSummary(result, resultType, selectedLanguage);
        } catch (error) {
            console.error('Error generating speech summary:', error);
            return selectedLanguage === 'hi' ? 'परिणाम का सारांश उपलब्ध नहीं है।' :
                   selectedLanguage === 'mr' ? 'निकालाचा सारांश उपलब्ध नाही.' :
                   selectedLanguage === 'gu' ? 'પરિણામનો સારાંશ ઉપલબ્ધ નથી.' :
                   selectedLanguage === 'ta' ? 'முடிவுகளின் சுருக்கம் கிடைக்கவில்லை.' :
                   'Summary not available.';
        }
    }, [result, resultType, selectedLanguage]);

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
                        <Volume2 className="w-5 h-5 text-blue-600" />
                        <h3 className="header-title">{title}</h3>
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
                    {compact && !isExpanded && (
                        <div className="compact-preview">
                            <span className="preview-text">
                                Click to access audio summary in {resultSummaryGenerator.getAvailableLanguages()[selectedLanguage] || 'English'}
                            </span>
                        </div>
                    )}
                </div>
            )}

            {/* Content */}
            {(!compact || isExpanded) && (
                <div className="voice-summary-content">
                    {/* Language Selection */}
                    <VoiceLanguageSelector
                        selectedLanguage={selectedLanguage}
                        onLanguageChange={handleLanguageChange}
                        compact={compact}
                        showLabel={!compact}
                    />

                    {/* Speech Controls */}
                    <SpeechControls
                        text={cleanSpeechText}
                        language={selectedLanguage}
                        resultType={resultType}
                        autoPlay={autoPlay}
                        showSettings={!compact}
                        className={compact ? 'compact' : ''}
                        onStart={onSpeechStart}
                        onEnd={onSpeechEnd}
                        onError={onSpeechError}
                    />

                    {/* Summary Preview */}
                    {!compact && speechText && (
                        <div className="summary-preview">
                            <div className="preview-header">
                                <MessageSquare className="w-4 h-4" />
                                <span>Summary Preview</span>
                            </div>
                            <div className="preview-content">
                                <p className="preview-text">
                                    {speechText.length > 200 
                                        ? speechText.substring(0, 200) + '...'
                                        : speechText
                                    }
                                </p>
                                {speechText.length > 200 && (
                                    <button 
                                        className="show-more-btn"
                                        onClick={() => {
                                            const previewEl = document.querySelector('.preview-text');
                                            if (previewEl) {
                                                previewEl.textContent = speechText;
                                                previewEl.nextElementSibling?.remove();
                                            }
                                        }}
                                    >
                                        Show full text
                                    </button>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Accessibility Info */}
                    {!compact && (
                        <div className="accessibility-info">
                            <small className="accessibility-text">
                                🎧 Use headphones for better audio quality. 
                                Speech speed and volume can be adjusted in settings.
                                {selectedLanguage === 'hi' && (
                                    <> 
                                        <br />🇮🇳 <strong>Hindi not working?</strong> 
                                        <button 
                                            className="hindi-help-btn"
                                            onClick={() => {
                                                console.log('🔍 Hindi Voice Debug - Check console for details');
                                                console.log('💡 See HINDI_VOICE_SETUP.md for detailed instructions');
                                                console.log('📱 Quick fix: Install Hindi language pack in your OS');
                                                if (voiceService && voiceService.testHindiSpeech) {
                                                    voiceService.testHindiSpeech();
                                                } else {
                                                    console.log('⚠️ Voice service not available for testing');
                                                    // Fallback test
                                                    const testUtterance = new SpeechSynthesisUtterance('नमस्ते, यह हिंदी का परीक्षण है।');
                                                    testUtterance.lang = 'hi-IN';
                                                    speechSynthesis.speak(testUtterance);
                                                }
                                            }}
                                        >
                                            Test Hindi Voice
                                        </button>
                                    </>
                                )}
                            </small>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default VoiceSummary;