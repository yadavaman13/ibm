/**
 * Test Script for Voice Features
 * Run this in browser console to test voice functionality
 */

// Test Voice Service
console.log('🎧 Testing Voice Service...');

// Import voice service (adjust path as needed)
// import voiceService from '../src/services/voiceService.js';

// Test basic functionality
const testVoiceService = () => {
    console.log('Voice Service Tests:');
    console.log('- Supported:', voiceService.isSupported());
    console.log('- Available languages:', voiceService.getSupportedLanguages());
    
    // Test voices for each language
    ['en', 'hi', 'mr', 'gu', 'ta'].forEach(lang => {
        const voices = voiceService.getVoicesForLanguage(lang);
        console.log(`- ${lang} voices:`, voices.length);
    });
};

// Test Result Summary Generator
const testSummaryGenerator = () => {
    console.log('\\nSummary Generator Tests:');
    
    // Sample yield prediction result
    const sampleYieldResult = {
        predicted_yield: 2.5,
        model_confidence: 0.87,
        input_params: {
            crop: 'Rice',
            state: 'Punjab',
            season: 'Kharif'
        },
        factors_affecting: [
            { factor: 'Fertilizer usage' },
            { factor: 'Weather conditions' }
        ],
        recommendations: [
            'Use organic fertilizers',
            'Monitor soil moisture levels'
        ]
    };
    
    // Test summary generation in different languages
    ['en', 'hi', 'mr', 'gu', 'ta'].forEach(lang => {
        try {
            const summary = resultSummaryGenerator.generateSummary(
                sampleYieldResult, 
                'yieldPrediction', 
                lang
            );
            console.log(`- ${lang} summary length:`, summary.length, 'chars');
        } catch (error) {
            console.error(`- ${lang} error:`, error.message);
        }
    });
};

// Test speech synthesis
const testSpeechSynthesis = async () => {
    console.log('\\nSpeech Synthesis Test:');
    
    const testText = 'Hello, this is a test of the voice synthesis system.';
    
    try {
        console.log('- Starting speech test...');
        await voiceService.speak(testText, 'en', {
            rate: 1.0,
            pitch: 1.0,
            volume: 0.8,
            onStart: () => console.log('  Speech started'),
            onEnd: () => console.log('  Speech ended'),
            onError: (error) => console.error('  Speech error:', error)
        });
    } catch (error) {
        console.error('- Speech test failed:', error.message);
    }
};

// Sample disease detection result for testing
const sampleDiseaseResult = {
    detected_disease: {
        name: 'Leaf Blight',
        confidence: 0.92,
        symptoms: ['Brown spots on leaves', 'Yellowing margins'],
        causes: ['Fungal infection', 'High humidity'],
        crops_affected: ['Rice', 'Wheat']
    },
    estimated_severity: 'moderate',
    crop_type: 'Rice',
    location: 'Punjab',
    timestamp: new Date().toISOString(),
    treatment_plan: {
        steps: [
            'Apply fungicide spray',
            'Improve field drainage',
            'Remove affected leaves'
        ]
    }
};

// Test disease detection summary
const testDiseaseDetectionSummary = () => {
    console.log('\\nDisease Detection Summary Test:');
    
    ['en', 'hi', 'mr', 'gu', 'ta'].forEach(lang => {
        try {
            const summary = resultSummaryGenerator.generateSummary(
                sampleDiseaseResult,
                'diseaseDetection',
                lang
            );
            console.log(`- ${lang} disease summary length:`, summary.length, 'chars');
            if (lang === 'en') {
                console.log('- English sample:', summary.substring(0, 100) + '...');
            }
        } catch (error) {
            console.error(`- ${lang} error:`, error.message);
        }
    });
};

// Run all tests
const runAllTests = () => {
    console.log('🚀 Running Voice Feature Tests...');
    console.log('=====================================');
    
    // Only run if voice service is available
    if (typeof voiceService !== 'undefined') {
        testVoiceService();
    } else {
        console.log('⚠️ voiceService not available in global scope');
    }
    
    if (typeof resultSummaryGenerator !== 'undefined') {
        testSummaryGenerator();
        testDiseaseDetectionSummary();
    } else {
        console.log('⚠️ resultSummaryGenerator not available in global scope');
    }
    
    console.log('\\n✅ Tests completed!');
    console.log('💡 To test speech synthesis, call testSpeechSynthesis()');
};

// Browser-specific tests
const testBrowserSupport = () => {
    console.log('\\nBrowser Support Tests:');
    console.log('- speechSynthesis:', 'speechSynthesis' in window);
    console.log('- SpeechSynthesisUtterance:', 'SpeechSynthesisUtterance' in window);
    console.log('- User agent:', navigator.userAgent);
    
    if ('speechSynthesis' in window) {
        const voices = speechSynthesis.getVoices();
        console.log('- Total voices available:', voices.length);
        
        // Group by language
        const languageMap = {};
        voices.forEach(voice => {
            const lang = voice.lang.split('-')[0];
            if (!languageMap[lang]) languageMap[lang] = 0;
            languageMap[lang]++;
        });
        
        console.log('- Voices by language:', languageMap);
    }
};

// Export test functions for manual use
window.voiceTests = {
    runAllTests,
    testVoiceService,
    testSummaryGenerator,
    testSpeechSynthesis,
    testDiseaseDetectionSummary,
    testBrowserSupport
};

// Auto-run basic tests
runAllTests();
testBrowserSupport();

console.log('\\n📝 Available test functions:');
console.log('- voiceTests.runAllTests()');
console.log('- voiceTests.testSpeechSynthesis()');
console.log('- voiceTests.testBrowserSupport()');