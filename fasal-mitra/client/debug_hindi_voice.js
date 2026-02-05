/**
 * Hindi Voice Troubleshooting Guide
 * 
 * If Hindi voice is not working properly, try these solutions:
 */

// Helper function to debug voice issues
const debugHindiVoice = () => {
    console.log('🔍 Hindi Voice Debugging Guide');
    console.log('================================');
    
    // Check if speech synthesis is supported
    if (!('speechSynthesis' in window)) {
        console.error('❌ Speech Synthesis not supported in this browser');
        console.log('💡 Try using Chrome, Firefox, or Edge instead');
        return;
    }
    
    // Get all available voices
    const voices = speechSynthesis.getVoices();
    console.log(`📊 Total voices available: ${voices.length}`);
    
    // Check for Hindi voices
    const hindiVoices = voices.filter(voice => 
        voice.lang.toLowerCase().includes('hi') || 
        voice.name.toLowerCase().includes('hindi')
    );
    
    console.log(`🇮🇳 Hindi voices found: ${hindiVoices.length}`);
    
    if (hindiVoices.length > 0) {
        console.log('✅ Hindi voices available:');
        hindiVoices.forEach((voice, index) => {
            console.log(`  ${index + 1}. ${voice.name} (${voice.lang}) - Local: ${voice.localService}`);
        });
    } else {
        console.log('❌ No Hindi voices found');
        console.log('');
        console.log('💡 Solutions to enable Hindi voice:');
        console.log('');
        console.log('🖥️  Windows:');
        console.log('   1. Go to Settings > Time & Language > Language');
        console.log('   2. Add Hindi language pack');
        console.log('   3. Under Hindi, click Options > Speech');
        console.log('   4. Download and install Hindi speech pack');
        console.log('   5. Restart browser');
        console.log('');
        console.log('🍎 macOS:');
        console.log('   1. Go to System Preferences > Accessibility > Speech');
        console.log('   2. Click "System Voice" dropdown');
        console.log('   3. Select "Customize" and download Hindi voices');
        console.log('   4. Restart browser');
        console.log('');
        console.log('🌍 Chrome Browser:');
        console.log('   1. Go to chrome://settings/languages');
        console.log('   2. Add Hindi language');
        console.log('   3. Enable "Use this language for spell check"');
        console.log('   4. Restart Chrome');
        console.log('');
        console.log('📱 Mobile:');
        console.log('   1. Go to device Settings > Language & Input');
        console.log('   2. Add Hindi as system language');
        console.log('   3. Enable Hindi TTS in Accessibility settings');
    }
    
    // Check browser-specific recommendations
    const userAgent = navigator.userAgent;
    if (userAgent.includes('Chrome')) {
        console.log('');
        console.log('🔧 Chrome-specific tips:');
        console.log('   - Chrome has the best Hindi TTS support');
        console.log('   - Make sure you\'re using Chrome 70+ for best results');
        console.log('   - Try enabling "Use system voice" in Chrome flags');
    } else if (userAgent.includes('Firefox')) {
        console.log('');
        console.log('🔧 Firefox-specific tips:');
        console.log('   - Firefox relies on system voices');
        console.log('   - Install Hindi language pack on your OS');
        console.log('   - Consider switching to Chrome for better Hindi support');
    } else if (userAgent.includes('Safari')) {
        console.log('');
        console.log('🔧 Safari-specific tips:');
        console.log('   - Safari has limited Hindi TTS support');
        console.log('   - Install Hindi voice in macOS System Preferences');
        console.log('   - Consider using Chrome or Firefox for better results');
    }
    
    // Test current voice selection
    console.log('');
    console.log('🧪 Testing current voice selection...');
    
    try {
        // Import voice service if available
        if (typeof voiceService !== 'undefined') {
            const debugInfo = voiceService.debugVoices();
            console.log('Voice service debug info:', debugInfo);
            
            const hindiTest = voiceService.getBestVoice('hi');
            if (hindiTest) {
                console.log(`✅ Voice service will use: ${hindiTest.name} (${hindiTest.lang})`);
            } else {
                console.log('⚠️  Voice service will fall back to English');
            }
        }
    } catch (error) {
        console.log('⚠️  Voice service not available in console context');
    }
    
    console.log('');
    console.log('🎯 Quick test:');
    console.log('Run: testHindiSpeech() to test Hindi voice');
};

// Quick test function
const testHindiSpeech = () => {
    const testText = 'नमस्ते, यह हिंदी आवाज का परीक्षण है।'; // "Hello, this is a Hindi voice test"
    
    const utterance = new SpeechSynthesisUtterance(testText);
    utterance.lang = 'hi-IN';
    
    const hindiVoices = speechSynthesis.getVoices().filter(voice => 
        voice.lang.toLowerCase().includes('hi')
    );
    
    if (hindiVoices.length > 0) {
        utterance.voice = hindiVoices[0];
        console.log(`🎵 Testing Hindi speech with: ${hindiVoices[0].name}`);
    } else {
        console.log('🎵 Testing Hindi speech with system default (may use English voice)');
    }
    
    utterance.onstart = () => console.log('▶️  Speech started');
    utterance.onend = () => console.log('⏹️  Speech ended');
    utterance.onerror = (e) => console.error('❌ Speech error:', e.error);
    
    speechSynthesis.speak(utterance);
};

// Auto-run debugging if voices are not loaded yet
if (speechSynthesis.getVoices().length === 0) {
    console.log('⏳ Waiting for voices to load...');
    speechSynthesis.onvoiceschanged = () => {
        console.log('🔄 Voices loaded, running debug...');
        debugHindiVoice();
    };
} else {
    debugHindiVoice();
}

// Make functions available globally for manual testing
window.debugHindiVoice = debugHindiVoice;
window.testHindiSpeech = testHindiSpeech;

console.log('');
console.log('📝 Available functions:');
console.log('- debugHindiVoice() - Run voice diagnostics');
console.log('- testHindiSpeech() - Test Hindi speech synthesis');