/**
 * VoiceService - Abstraction layer for Text-to-Speech functionality
 * Supports multiple languages and provides fallback mechanisms
 */

class VoiceService {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.currentUtterance = null;
        this.supported = 'speechSynthesis' in window;
        this.isPlaying = false;
        this.isPaused = false;
        
        // Language mappings for Web Speech API with fallbacks
        this.languageMap = {
            'en': ['en-US', 'en-GB', 'en'],
            'hi': ['hi-IN', 'hi', 'en-US'], // Fallback to English if Hindi not available
            'mr': ['mr-IN', 'mr', 'hi-IN', 'en-US'],
            'gu': ['gu-IN', 'gu', 'hi-IN', 'en-US'],
            'ta': ['ta-IN', 'ta', 'en-US']
        };

        // Initialize voices when available
        this.initializeVoices();
    }

    /**
     * Initialize available voices
     */
    initializeVoices() {
        if (!this.supported) return;

        const loadVoices = () => {
            this.voices = this.synthesis.getVoices();
        };

        loadVoices();
        
        // Some browsers load voices asynchronously
        if (this.synthesis.onvoiceschanged !== undefined) {
            this.synthesis.onvoiceschanged = loadVoices;
        }
    }

    /**
     * Get available voices for a specific language
     * @param {string} language - Language code (en, hi, mr, gu, ta)
     * @returns {SpeechSynthesisVoice[]}
     */
    getVoicesForLanguage(language) {
        if (!this.supported) return [];
        
        const langCodes = this.languageMap[language] || [language];
        
        for (const langCode of langCodes) {
            const voices = this.voices.filter(voice => {
                const voiceLang = voice.lang.toLowerCase();
                const targetLang = langCode.toLowerCase();
                
                return voiceLang === targetLang || 
                       voiceLang.startsWith(targetLang.split('-')[0]) ||
                       (targetLang.includes('-') && voiceLang.startsWith(targetLang));
            });
            
            if (voices.length > 0) {
                console.log(`Found ${voices.length} voices for ${language} (${langCode}):`, voices.map(v => v.name));
                return voices;
            }
        }
        
        console.warn(`No voices found for language: ${language}`);
        return [];
    }

    /**
     * Get the best voice for a language
     * @param {string} language - Language code
     * @returns {SpeechSynthesisVoice|null}
     */
    getBestVoice(language) {
        const availableVoices = this.getVoicesForLanguage(language);
        
        if (availableVoices.length === 0) {
            console.warn(`No voices available for ${language}, falling back to English`);
            const fallbackVoices = this.getVoicesForLanguage('en');
            return fallbackVoices[0] || null;
        }

        // Prioritize voices: local > Google > Microsoft > others
        const prioritizeVoice = (voice) => {
            const name = voice.name.toLowerCase();
            if (voice.localService) return 4;
            if (name.includes('google')) return 3;
            if (name.includes('microsoft') || name.includes('david') || name.includes('zira')) return 2;
            return 1;
        };
        
        availableVoices.sort((a, b) => prioritizeVoice(b) - prioritizeVoice(a));
        
        const selectedVoice = availableVoices[0];
        console.log(`Selected voice for ${language}:`, selectedVoice.name, `(${selectedVoice.lang})`);
        return selectedVoice;
    }

    /**
     * Speak text in specified language
     * @param {string} text - Text to speak
     * @param {string} language - Language code (default: 'en')
     * @param {Object} options - Speech options
     * @returns {Promise<void>}
     */
    speak(text, language = 'en', options = {}) {
        return new Promise((resolve, reject) => {
            if (!this.supported) {
                reject(new Error('Speech synthesis not supported'));
                return;
            }

            // Stop any current speech
            this.stop();

            const utterance = new SpeechSynthesisUtterance(text);
            const voice = this.getBestVoice(language);

            if (voice) {
                utterance.voice = voice;
                utterance.lang = voice.lang;
                console.log(`Speaking in ${language} using voice: ${voice.name} (${voice.lang})`);
            } else {
                const fallbackLang = this.languageMap[language]?.[0] || 'en-US';
                utterance.lang = fallbackLang;
                console.warn(`No voice found for ${language}, using lang: ${fallbackLang}`);
            }

            // Apply options
            utterance.rate = options.rate || 0.9;
            utterance.pitch = options.pitch || 1;
            utterance.volume = options.volume || 1;

            // Event handlers
            utterance.onstart = () => {
                this.isPlaying = true;
                this.isPaused = false;
                options.onStart && options.onStart();
            };

            utterance.onend = () => {
                this.isPlaying = false;
                this.isPaused = false;
                this.currentUtterance = null;
                options.onEnd && options.onEnd();
                resolve();
            };

            utterance.onerror = (event) => {
                this.isPlaying = false;
                this.isPaused = false;
                this.currentUtterance = null;
                options.onError && options.onError(event);
                reject(new Error(`Speech synthesis error: ${event.error}`));
            };

            utterance.onpause = () => {
                this.isPaused = true;
                options.onPause && options.onPause();
            };

            utterance.onresume = () => {
                this.isPaused = false;
                options.onResume && options.onResume();
            };

            this.currentUtterance = utterance;
            this.synthesis.speak(utterance);
        });
    }

    /**
     * Pause current speech
     */
    pause() {
        if (this.supported && this.isPlaying && !this.isPaused) {
            this.synthesis.pause();
        }
    }

    /**
     * Resume paused speech
     */
    resume() {
        if (this.supported && this.isPaused) {
            this.synthesis.resume();
        }
    }

    /**
     * Stop current speech
     */
    stop() {
        if (this.supported) {
            this.synthesis.cancel();
            this.isPlaying = false;
            this.isPaused = false;
            this.currentUtterance = null;
        }
    }

    /**
     * Check if speech is currently active
     * @returns {boolean}
     */
    isSpeaking() {
        return this.isPlaying;
    }

    /**
     * Check if speech is paused
     * @returns {boolean}
     */
    getPaused() {
        return this.isPaused;
    }

    /**
     * Get supported languages
     * @returns {string[]}
     */
    getSupportedLanguages() {
        if (!this.supported) return ['en']; // Always include English as fallback
        
        const supportedLangs = [];
        
        // Check each language for available voices
        Object.keys(this.languageMap).forEach(lang => {
            const voices = this.getVoicesForLanguage(lang);
            if (voices.length > 0) {
                supportedLangs.push(lang);
            } else {
                console.log(`Language ${lang} not supported - no voices available`);
            }
        });
        
        // Always include English as fallback
        if (!supportedLangs.includes('en')) {
            supportedLangs.push('en');
        }
        
        console.log('Supported languages:', supportedLangs);
        return supportedLangs;
    }

    /**
     * Check if browser supports speech synthesis
     * @returns {boolean}
     */
    isSupported() {
        return this.supported;
    }
    
    /**
     * Debug method to list all available voices
     * @returns {Object}
     */
    debugVoices() {
        if (!this.supported) {
            return { error: 'Speech synthesis not supported' };
        }
        
        const voicesByLanguage = {};
        
        this.voices.forEach(voice => {
            const lang = voice.lang.toLowerCase();
            if (!voicesByLanguage[lang]) {
                voicesByLanguage[lang] = [];
            }
            voicesByLanguage[lang].push({
                name: voice.name,
                lang: voice.lang,
                localService: voice.localService,
                voiceURI: voice.voiceURI
            });
        });
        
        return {
            totalVoices: this.voices.length,
            supportedLanguages: this.getSupportedLanguages(),
            voicesByLanguage,
            hindiVoices: voicesByLanguage['hi-in'] || voicesByLanguage['hi'] || []
        };
    }
    
    /**
     * Test Hindi speech functionality
     * @returns {Promise<boolean>}
     */
    async testHindiSpeech() {
        const testText = 'नमस्ते, यह हिंदी आवाज़ का परीक्षण है।';
        
        try {
            await this.speak(testText, 'hi', {
                rate: 0.8,
                onStart: () => console.log('🎵 Hindi speech test started'),
                onEnd: () => console.log('✅ Hindi speech test completed'),
                onError: (error) => console.error('❌ Hindi speech test failed:', error)
            });
            return true;
        } catch (error) {
            console.error('❌ Hindi speech test failed:', error.message);
            return false;
        }
    }
}

// Create singleton instance
const voiceService = new VoiceService();

export default voiceService;