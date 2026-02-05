# 🇮🇳 Hindi Voice Support Guide

## Quick Fix for Hindi Voice Issues

### Why Hindi Voice Might Not Work

The Hindi voice feature depends on your browser and operating system having Hindi text-to-speech (TTS) support installed. Many systems don't have this by default.

### ✅ Quick Solutions

#### 🖥️ **Windows Users**
1. **Open Settings** → `Time & Language` → `Language`
2. **Add Hindi** if not already added
3. **Click on Hindi** → `Options`
4. **Under Speech**, download the Hindi speech pack
5. **Restart your browser**

#### 🍎 **Mac Users**
1. **System Preferences** → `Accessibility` → `Speech`
2. **System Voice dropdown** → `Customize`
3. **Download Hindi voices** (look for "Lekha" or other Hindi voices)
4. **Restart your browser**

#### 🌐 **Chrome Users (Best Option)**
1. Go to `chrome://settings/languages`
2. **Add Hindi language**
3. Enable **"Use this language for spell check"**
4. **Restart Chrome**

#### 📱 **Mobile Users**
1. **Device Settings** → `Language & Input`
2. **Add Hindi** as system language
3. **Accessibility Settings** → Enable Hindi TTS

### 🧪 Testing Hindi Voice

Open browser console (F12) and run:

```javascript
// Test if Hindi voices are available
const voices = speechSynthesis.getVoices();
const hindiVoices = voices.filter(v => v.lang.includes('hi'));
console.log('Hindi voices:', hindiVoices.length);

// Quick test
const utterance = new SpeechSynthesisUtterance('नमस्ते');
utterance.lang = 'hi-IN';
speechSynthesis.speak(utterance);
```

### 🔧 Troubleshooting

#### Problem: "Using English voice" message appears
**Solution**: Your system doesn't have Hindi TTS installed. Follow the installation steps above.

#### Problem: Hindi text plays but in English pronunciation  
**Solution**: Install native Hindi voice pack on your OS, don't rely on browser-only solutions.

#### Problem: No sound at all
**Solution**: 
1. Check browser permissions for audio
2. Ensure speakers/headphones are connected
3. Try a different browser (Chrome recommended)

#### Problem: Choppy or robotic Hindi voice
**Solution**: 
1. Reduce speech speed in controls
2. Close other browser tabs
3. Install higher-quality Hindi voice pack

### 🏆 Best Browser Support

| Browser | Hindi Support | Recommendation |
|---------|---------------|----------------|
| **Chrome** | ⭐⭐⭐⭐⭐ | Best choice |
| **Edge** | ⭐⭐⭐⭐ | Good on Windows |
| **Firefox** | ⭐⭐⭐ | Relies on system voices |
| **Safari** | ⭐⭐ | Limited support |

### 💡 Pro Tips

1. **Chrome is best** for Hindi TTS - it has built-in fallback voices
2. **Install OS language pack** rather than relying on browser only  
3. **Use headphones** for better audio quality
4. **Adjust speed** if Hindi sounds too fast
5. **Test with short phrases** first

### 🚀 Advanced Setup

For developers wanting to test Hindi voice programmatically:

```javascript
// Load the debug script
// Copy and paste debug_hindi_voice.js content in browser console

// Then run:
debugHindiVoice();  // Shows detailed diagnostics
testHindiSpeech();  // Tests actual Hindi speech
```

### 🆘 Still Having Issues?

1. **Check browser console** for error messages (F12)
2. **Try the debug script** provided in `/client/debug_hindi_voice.js`
3. **Test on different browser** (Chrome recommended)  
4. **Verify system languages** include Hindi
5. **Restart computer** after installing language packs

---

**🎯 Quick Test**: Visit Yield Prediction page, generate results, select Hindi from voice dropdown, and click play. If you hear Hindi pronunciation, you're all set! If it sounds like English, follow the installation steps above.