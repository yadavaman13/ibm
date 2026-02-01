"""Test Gemini API connection"""
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

api_key = os.getenv('GEMINI_API_KEY', '')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found!")
print(f"API Key length: {len(api_key)}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # List available models
        print("\nAvailable models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Test with gemini-2.5-flash
        print("\n🧪 Testing gemini-2.5-flash...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say hello in one word")
        print(f"✅ Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
else:
    print("❌ No API key found in .env file")
