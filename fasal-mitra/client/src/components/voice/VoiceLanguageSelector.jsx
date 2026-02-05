import React, { useState, useEffect } from 'react';
import { Languages, ChevronDown } from 'lucide-react';
import voiceService from '../../services/voiceService';
import resultSummaryGenerator from '../../utils/resultSummaryGenerator';
import './VoiceLanguageSelector.css';

const VoiceLanguageSelector = ({ 
    selectedLanguage = 'en', 
    onLanguageChange = () => {},
    compact = false,
    showLabel = true,
    className = ''
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [supportedLanguages, setSupportedLanguages] = useState([]);
    const [availableLanguages, setAvailableLanguages] = useState({});

    useEffect(() => {
        // Get supported languages from voice service
        const supported = voiceService.getSupportedLanguages();
        setSupportedLanguages(supported);
        
        // Get language names from result summary generator
        const languages = resultSummaryGenerator.getAvailableLanguages();
        setAvailableLanguages(languages);
    }, []);

    const handleLanguageSelect = (language) => {
        onLanguageChange(language);
        setIsOpen(false);
    };

    const handleKeyDown = (event, language) => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            handleLanguageSelect(language);
        }
    };

    // Get flag emoji for language
    const getFlagEmoji = (langCode) => {
        const flags = {
            'en': '🇺🇸',
            'hi': '🇮🇳',
            'mr': '🇮🇳',
            'gu': '🇮🇳',
            'ta': '🇮🇳'
        };
        return flags[langCode] || '🌐';
    };

    // Check if language has native voice support
    const hasNativeVoice = (langCode) => {
        const voices = voiceService.getVoicesForLanguage(langCode);
        return voices.some(voice => voice.lang.toLowerCase().startsWith(langCode));
    };

    // Get language status
    const getLanguageStatus = (langCode) => {
        if (langCode === 'en') return 'supported';
        
        const voices = voiceService.getVoicesForLanguage(langCode);
        if (voices.length === 0) return 'fallback';
        
        const hasNative = voices.some(voice => 
            voice.lang.toLowerCase().startsWith(langCode) || 
            voice.lang.toLowerCase().includes(langCode)
        );
        
        return hasNative ? 'supported' : 'fallback';
    };

    // Filter available languages to show all languages with status
    const displayLanguages = Object.entries(availableLanguages)
        .sort(([a], [b]) => {
            // Always put English first, then alphabetical
            if (a === 'en') return -1;
            if (b === 'en') return 1;
            return a.localeCompare(b);
        });

    if (displayLanguages.length === 0) {
        return (
            <div className={`voice-language-selector unsupported ${className}`}>
                <div className="unsupported-text">
                    <Languages className="w-4 h-4" />
                    <span>No voice languages available</span>
                </div>
            </div>
        );
    }

    return (
        <div className={`voice-language-selector ${compact ? 'compact' : ''} ${className}`}>
            {showLabel && !compact && (
                <label className="selector-label">
                    <Languages className="w-4 h-4" />
                    <span>Voice Language:</span>
                </label>
            )}
            
            <div className="dropdown-container">
                <button
                    className="dropdown-trigger"
                    onClick={() => setIsOpen(!isOpen)}
                    onBlur={() => setTimeout(() => setIsOpen(false), 150)}
                    aria-expanded={isOpen}
                    aria-haspopup="listbox"
                    role="combobox"
                >
                    <div className="selected-language">
                        <span className="flag">{getFlagEmoji(selectedLanguage)}</span>
                        <span className="language-name">
                            {availableLanguages[selectedLanguage] || 'Select Language'}
                        </span>
                    </div>
                    <ChevronDown className={`chevron ${isOpen ? 'open' : ''}`} />
                </button>

                {isOpen && (
                    <div className="dropdown-menu" role="listbox">
                        {displayLanguages.map(([code, name]) => {
                            const status = getLanguageStatus(code);
                            return (
                                <div
                                    key={code}
                                    className={`dropdown-item ${selectedLanguage === code ? 'selected' : ''} ${status === 'fallback' ? 'fallback' : ''}`}
                                    onClick={() => handleLanguageSelect(code)}
                                    onKeyDown={(e) => handleKeyDown(e, code)}
                                    role="option"
                                    aria-selected={selectedLanguage === code}
                                    tabIndex={0}
                                >
                                    <span className="flag">{getFlagEmoji(code)}</span>
                                    <span className="language-info">
                                        <span className="language-name">{name}</span>
                                        {status === 'fallback' && (
                                            <span className="fallback-note">Will use English voice</span>
                                        )}
                                    </span>
                                    {selectedLanguage === code && (
                                        <span className="check-mark">✓</span>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* Language support status */}
            <div className="support-status">
                <span className="status-text">
                    {(() => {
                        const status = getLanguageStatus(selectedLanguage);
                        if (status === 'supported') {
                            return (
                                <>
                                    <span className="status-indicator supported">●</span> 
                                    Native voice available
                                </>
                            );
                        } else {
                            return (
                                <>
                                    <span className="status-indicator fallback">●</span> 
                                    Using English voice
                                </>
                            );
                        }
                    })()} 
                </span>
                {selectedLanguage === 'hi' && getLanguageStatus('hi') === 'fallback' && (
                    <div className="hindi-help">
                        <small>
                            💡 For Hindi voice: Install Hindi language pack in Windows/Mac, 
                            or try Chrome with Hindi language support enabled.
                        </small>
                    </div>
                )}
            </div>
        </div>
    );
};

export default VoiceLanguageSelector;