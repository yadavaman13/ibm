import React, { useState, useEffect } from 'react';
import { Play, Pause, Square, Volume2, VolumeX, Settings } from 'lucide-react';
import voiceService from '../../services/voiceService';
import './SpeechControls.css';

const SpeechControls = ({ 
    text, 
    language = 'en', 
    resultType = 'general',
    autoPlay = false,
    showSettings = true,
    className = '',
    onStart = () => {},
    onEnd = () => {},
    onError = () => {}
}) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [showSettingsPanel, setShowSettingsPanel] = useState(false);
    const [speechSettings, setSpeechSettings] = useState({
        rate: 0.9,
        pitch: 1.0,
        volume: 1.0
    });
    const [error, setError] = useState(null);

    // Check if speech synthesis is supported
    const [isSupported, setIsSupported] = useState(false);

    useEffect(() => {
        setIsSupported(voiceService.isSupported());
    }, []);

    useEffect(() => {
        if (autoPlay && text && isSupported) {
            handlePlay();
        }
    }, [text, autoPlay, isSupported]);

    const handlePlay = async () => {
        if (!text || !isSupported) {
            setError('Speech synthesis not supported or no text provided');
            return;
        }

        if (isPaused) {
            voiceService.resume();
            setIsPaused(false);
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            await voiceService.speak(text, language, {
                rate: speechSettings.rate,
                pitch: speechSettings.pitch,
                volume: speechSettings.volume,
                onStart: () => {
                    setIsPlaying(true);
                    setIsLoading(false);
                    onStart();
                },
                onEnd: () => {
                    setIsPlaying(false);
                    setIsPaused(false);
                    onEnd();
                },
                onError: (event) => {
                    setError(`Speech error: ${event.error}`);
                    setIsPlaying(false);
                    setIsLoading(false);
                    onError(event);
                },
                onPause: () => {
                    setIsPaused(true);
                },
                onResume: () => {
                    setIsPaused(false);
                }
            });
        } catch (err) {
            setError(err.message);
            setIsPlaying(false);
            setIsLoading(false);
            onError(err);
        }
    };

    const handlePause = () => {
        if (isPlaying && !isPaused) {
            voiceService.pause();
            setIsPaused(true);
        }
    };

    const handleStop = () => {
        voiceService.stop();
        setIsPlaying(false);
        setIsPaused(false);
        setIsLoading(false);
    };

    const handleSettingsChange = (setting, value) => {
        setSpeechSettings(prev => ({
            ...prev,
            [setting]: value
        }));
    };

    // Don't render if not supported
    if (!isSupported) {
        return (
            <div className={`speech-controls unsupported ${className}`}>
                <div className="unsupported-message">
                    <VolumeX className="w-4 h-4" />
                    <span>Speech synthesis not supported in this browser</span>
                </div>
            </div>
        );
    }

    return (
        <div className={`speech-controls ${className}`}>
            <div className="controls-main">
                <div className="playback-controls">
                    {!isPlaying && !isLoading ? (
                        <button
                            onClick={handlePlay}
                            disabled={!text}
                            className="control-btn play-btn"
                            title="Play summary"
                        >
                            <Play className="w-4 h-4" />
                        </button>
                    ) : isLoading ? (
                        <div className="loading-spinner">
                            <div className="spinner"></div>
                        </div>
                    ) : isPaused ? (
                        <button
                            onClick={handlePlay}
                            className="control-btn resume-btn"
                            title="Resume"
                        >
                            <Play className="w-4 h-4" />
                        </button>
                    ) : (
                        <button
                            onClick={handlePause}
                            className="control-btn pause-btn"
                            title="Pause"
                        >
                            <Pause className="w-4 h-4" />
                        </button>
                    )}

                    <button
                        onClick={handleStop}
                        disabled={!isPlaying && !isPaused}
                        className="control-btn stop-btn"
                        title="Stop"
                    >
                        <Square className="w-4 h-4" />
                    </button>
                </div>

                <div className="speech-info">
                    <Volume2 className="w-4 h-4 text-gray-500" />
                    <span className="speech-status">
                        {isLoading ? 'Loading...' :
                         isPlaying && !isPaused ? 'Playing' :
                         isPaused ? 'Paused' :
                         'Ready'}
                    </span>
                </div>

                {showSettings && (
                    <button
                        onClick={() => setShowSettingsPanel(!showSettingsPanel)}
                        className="control-btn settings-btn"
                        title="Speech settings"
                    >
                        <Settings className="w-4 h-4" />
                    </button>
                )}
            </div>

            {/* Settings Panel */}
            {showSettingsPanel && (
                <div className="settings-panel">
                    <div className="settings-row">
                        <label>Speed</label>
                        <input
                            type="range"
                            min="0.5"
                            max="2"
                            step="0.1"
                            value={speechSettings.rate}
                            onChange={(e) => handleSettingsChange('rate', parseFloat(e.target.value))}
                            className="range-input"
                        />
                        <span className="setting-value">{speechSettings.rate}x</span>
                    </div>

                    <div className="settings-row">
                        <label>Pitch</label>
                        <input
                            type="range"
                            min="0.5"
                            max="2"
                            step="0.1"
                            value={speechSettings.pitch}
                            onChange={(e) => handleSettingsChange('pitch', parseFloat(e.target.value))}
                            className="range-input"
                        />
                        <span className="setting-value">{speechSettings.pitch}</span>
                    </div>

                    <div className="settings-row">
                        <label>Volume</label>
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.1"
                            value={speechSettings.volume}
                            onChange={(e) => handleSettingsChange('volume', parseFloat(e.target.value))}
                            className="range-input"
                        />
                        <span className="setting-value">{Math.round(speechSettings.volume * 100)}%</span>
                    </div>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="speech-error">
                    <span className="error-text">{error}</span>
                    <button 
                        onClick={() => setError(null)} 
                        className="error-close"
                        title="Clear error"
                    >
                        ×
                    </button>
                </div>
            )}
        </div>
    );
};

export default SpeechControls;