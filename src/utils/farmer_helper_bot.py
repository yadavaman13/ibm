"""
Farmer Helper Chatbot Component

Provides contextual help for technical farming terms using Google Gemini AI.
Helps farmers understand terminologies, measurement methods, and provides learning resources.
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import time
from datetime import datetime

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class FarmerHelperBot:
    """AI-powered helper bot to explain farming terminology to farmers."""
    
    def __init__(self):
        """Initialize the helper bot with Gemini API."""
        self.api_key = os.getenv('GEMINI_API_KEY', '').strip()
        self.last_request_time = None
        self.min_request_interval = 15  # 15 seconds between requests
        self.request_count = 0
        self.max_requests_per_minute = 4  # Conservative limit
        
        if self.api_key and self.api_key != 'your_gemini_api_key_here' and len(self.api_key) > 10:
            try:
                genai.configure(api_key=self.api_key)
                # Use gemini-pro instead of gemini-2.5-flash for better rate limits
                self.model = genai.GenerativeModel('gemini-pro')
                self.enabled = True
                print("DEBUG: Gemini API configured with gemini-pro model")
            except Exception as e:
                print(f"DEBUG: Error configuring Gemini API: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def _can_make_request(self):
        """Check if we can make a request without hitting rate limits."""
        current_time = time.time()
        
        # Reset request count every minute
        if self.last_request_time and (current_time - self.last_request_time) > 60:
            self.request_count = 0
        
        # Check if we've exceeded our per-minute limit
        if self.request_count >= self.max_requests_per_minute:
            return False
            
        # Check minimum interval between requests
        if self.last_request_time and (current_time - self.last_request_time) < self.min_request_interval:
            return False
            
        return True
    
    def get_term_explanation(self, term, context="farming"):
        """
        Get explanation for a technical farming term with rate limiting.
        """
        if not self.enabled:
            return self._get_fallback_explanation(term)
        
        # Check rate limits
        if not self._can_make_request():
            return {
                'simple_explanation': f"⏳ Rate limit reached. Please wait a moment before asking about '{term}' again.",
                'why_important': "Rate limiting helps prevent API quota exhaustion.",
                'how_to_measure': "Please wait 15 seconds between requests.",
                'typical_values': "API allows limited requests per minute.",
                'video_search': f"{term} farming",
                'tips': ["Wait 15 seconds between questions", "Ask detailed questions to get complete answers"],
                'rate_limited': True
            }
        
        try:
            prompt = f"""You are a helpful farming assistant. Explain "{term}" in simple language suitable for farmers.

Keep the response short (2-3 sentences) and practical. Focus on:
1. What it means in farming
2. Why it matters to farmers
3. One practical tip

Term: {term}
Context: {context}
"""

            response = self.model.generate_content(prompt)
            
            # Update rate limiting counters
            self.last_request_time = time.time()
            self.request_count += 1
            
            # Convert AI response to expected format
            return {
                'simple_explanation': response.text,
                'why_important': "Understanding this helps you make better farming decisions.",
                'how_to_measure': "Consult with local agriculture experts for measurement methods.",
                'typical_values': "Values vary by crop and region.",
                'video_search': f"{term} farming india",
                'tips': ["Consult local krishi vigyan kendra", "Keep records of observations"],
                'rate_limited': False
            }
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return {
                    'simple_explanation': f"⏳ API quota exceeded. Please try again later for '{term}'.",
                    'why_important': "Free API has daily usage limits.",
                    'how_to_measure': "Wait for quota to reset (usually 24 hours).",
                    'typical_values': "Free tier: 20 requests per day",
                    'video_search': f"{term} farming",
                    'tips': ["Try again tomorrow", "Use fallback explanations for common terms"],
                    'rate_limited': True
                }
            else:
                return self._get_fallback_explanation(term)
    
    def _get_fallback_explanation(self, term, error=None):
        """Provide fallback explanation when API is not available."""
        fallback_terms = {
            "N": {
                "simple_explanation": "Nitrogen (N) is a nutrient that helps plants grow green and healthy. It's like protein for plants - helps them grow tall and produce more leaves.",
                "why_important": "Good nitrogen levels mean better crop growth and higher yields. Too little makes plants yellow and weak.",
                "how_to_measure": "1. Use a soil testing kit from agriculture office\n2. Send soil sample to testing lab\n3. Use nitrogen test strips (available at agri shops)\n4. Look for leaf color - dark green is good, yellow means low nitrogen",
                "typical_values": "Good range: 200-300 kg/ha. Below 150 is low, above 400 might be too much.",
                "video_search": "how to test soil nitrogen farming",
                "tips": ["Add organic manure to increase nitrogen", "Grow legumes (like peas) - they add nitrogen naturally", "Test soil before adding fertilizers"]
            },
            "P": {
                "simple_explanation": "Phosphorus (P) helps plants develop strong roots and flowers. Think of it as the energy booster that helps seeds germinate and flowers bloom.",
                "why_important": "Strong roots mean plants can find water better. Good for fruit and seed production.",
                "how_to_measure": "1. Get soil test from agriculture department\n2. Look at root development - weak roots may mean low P\n3. Use soil testing kit\n4. Purple color on leaves can indicate low phosphorus",
                "typical_values": "Good range: 15-25 kg/ha. Below 10 is low. Above 30 usually not needed.",
                "video_search": "phosphorus in soil farming india",
                "tips": ["Add bone meal or rock phosphate", "Don't overuse - phosphorus stays in soil long time", "Important during flowering and fruiting stage"]
            },
            "K": {
                "simple_explanation": "Potassium (K) makes plants strong and disease-resistant. Like vitamins for humans, it keeps crops healthy and helps them fight diseases.",
                "why_important": "Strong plants that can survive drought and diseases. Better quality fruits and grains.",
                "how_to_measure": "1. Soil test from krishi vigyan kendra\n2. Brown leaf edges might mean low potassium\n3. Use potassium test strips\n4. Weak stems indicate low K levels",
                "typical_values": "Good range: 120-180 kg/ha. Below 100 is low. Above 250 usually not needed.",
                "video_search": "potassium deficiency crops india",
                "tips": ["Wood ash is natural source of potassium", "Important during fruit development", "Helps plants use water efficiently"]
            },
            "Temperature": {
                "simple_explanation": "Temperature is how hot or cold the environment is. Different crops need different temperatures to grow well.",
                "why_important": "Right temperature means crops grow properly. Wrong temperature can damage crops or reduce yield.",
                "how_to_measure": "1. Use a simple thermometer\n2. Check weather apps on phone\n3. Note morning and evening temperatures\n4. Track maximum and minimum daily temperatures",
                "typical_values": "Varies by crop: Rice 25-35°C, Wheat 15-25°C, Tomato 18-27°C",
                "video_search": "optimal temperature for crops india",
                "tips": ["Plant at right season for your crop", "Use shade nets in extreme heat", "Mulching helps maintain soil temperature"]
            },
            "Rainfall": {
                "simple_explanation": "Rainfall is the amount of water that falls from the sky as rain. It's the main water source for most crops.",
                "why_important": "Right amount of rain at right time is crucial for good harvest. Too little or too much can damage crops.",
                "how_to_measure": "1. Use rain gauge (simple container)\n2. Check weather forecast\n3. Note rainy days in calendar\n4. Local agriculture office tracks rainfall",
                "typical_values": "Varies by crop: Rice needs 1200-1800mm, Wheat 400-600mm, Bajra 400-600mm per season",
                "video_search": "rainfall measurement farming india",
                "tips": ["Plan irrigation based on expected rainfall", "Collect rainwater for dry periods", "Choose crops suitable for your region's rainfall"]
            },
            "Humidity": {
                "simple_explanation": "Humidity is how much moisture is in the air. High humidity means the air feels wet and sticky.",
                "why_important": "High humidity can cause fungal diseases. Low humidity can dry out plants. Balance is important.",
                "how_to_measure": "1. Feel the air - sticky means high humidity\n2. Use humidity meter (available at electronics shops)\n3. Morning dew on leaves indicates high humidity\n4. Check weather reports",
                "typical_values": "Ideal: 60-70% for most crops. Above 80% increases disease risk. Below 40% can stress plants.",
                "video_search": "humidity effect on crops india",
                "tips": ["Good air circulation reduces high humidity", "Avoid watering in evening if humidity is high", "Some crops like rice prefer high humidity"]
            },
            "pH": {
                "simple_explanation": "pH tells if soil is acidic (sour like lemon) or alkaline (bitter like soap). Most crops like neutral soil (not too sour, not too bitter).",
                "why_important": "Wrong pH means plants can't absorb nutrients from soil, even if nutrients are present. Like having food you can't eat.",
                "how_to_measure": "1. Use pH test kit (available at agri shops)\n2. Soil testing lab will measure it\n3. Blue litmus paper turns red if soil is acidic\n4. Red litmus paper turns blue if soil is alkaline",
                "typical_values": "Good range: 6.0-7.5 (neutral). Below 5.5 is too acidic. Above 8.0 is too alkaline.",
                "video_search": "soil pH testing farming india",
                "tips": ["Add lime to increase pH (reduce acidity)", "Add sulfur to decrease pH (reduce alkalinity)", "Most vegetables like pH 6.0-7.0"]
            }
        }
        
        if term in fallback_terms:
            return fallback_terms[term]
        else:
            return {
                "simple_explanation": f"{term} is an important farming parameter that affects crop growth and yield.",
                "why_important": "Understanding this helps you make better farming decisions and improve your harvest.",
                "how_to_measure": "Consult with your local krishi vigyan kendra or agriculture officer for guidance on measuring this parameter.",
                "typical_values": "Values vary by crop and region. Check with local agriculture experts.",
                "video_search": f"{term} in farming india",
                "tips": ["Consult local agriculture experts", "Keep records of your observations", "Learn from experienced farmers in your area"]
            }
    
    def chat_with_farmer(self, user_question, conversation_history=None):
        """
        General farming chatbot conversation with rate limiting.
        """
        if not self.enabled:
            return "⚠️ Chatbot requires API key. Please check your .env file."
        
        # Check rate limits
        if not self._can_make_request():
            return "⏳ Please wait 15 seconds between questions to avoid API rate limits. Thank you for your patience!"
        
        try:
            # Build conversation context - shorter for rate limits
            context = """You are a helpful farming assistant. Give concise, practical advice in 2-3 sentences.
Use simple language suitable for farmers. Be encouraging and actionable.

"""
            
            # Limit conversation history to last 2 exchanges to save tokens
            if conversation_history and len(conversation_history) > 4:
                conversation_history = conversation_history[-4:]
            
            if conversation_history:
                for msg in conversation_history:
                    if msg['role'] == 'user':
                        context += f"Q: {msg['content']}\n"
                    else:
                        context += f"A: {msg['content']}\n"
            
            context += f"Q: {user_question}\nA:"
            
            response = self.model.generate_content(context)
            
            # Update rate limiting counters
            self.last_request_time = time.time()
            self.request_count += 1
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate" in error_msg.lower() or "429" in error_msg:
                return "⏳ API quota exceeded. Please try again in a few minutes. Thank you for your patience!"
            else:
                return f"⚠️ Sorry, I couldn't process your question right now. Please try again later."


def show_help_icon_with_chatbot(term, context="farming"):
    """
    Display a help expander with term explanation (works inside forms).
    
    Args:
        term: The technical term to explain
        context: Additional context
    """
    helper = FarmerHelperBot()
    
    # Create unique key for this term
    modal_key = f"help_{term.replace(' ', '_').replace('/', '_')}"
    
    # Use expander instead of button (works inside forms)
    with st.expander(f"❓ Learn about {term}", expanded=False):
        with st.spinner("🤔 Getting explanation..."):
            explanation = helper.get_term_explanation(term, context)
        
        # Simple explanation
        st.markdown("#### 🎯 What is it?")
        st.info(explanation['simple_explanation'])
        
        # Why important
        st.markdown("#### 💡 Why does it matter?")
        st.success(explanation['why_important'])
        
        # How to measure
        st.markdown("#### 📏 How to measure/find it?")
        st.markdown(explanation['how_to_measure'])
        
        # Typical values
        st.markdown("#### 📊 What are good values?")
        st.warning(explanation['typical_values'])
        
        # Tips
        if 'tips' in explanation:
            st.markdown("#### 💪 Quick Tips")
            for tip in explanation['tips']:
                st.markdown(f"• {tip}")
        
        # YouTube search link
        st.markdown("#### 📺 Learn More")
        youtube_query = explanation.get('video_search', f'{term} farming')
        youtube_url = f"https://www.youtube.com/results?search_query={youtube_query}"
        st.markdown(f"[🔍 Search YouTube: '{youtube_query}']({youtube_url})")


def show_general_chatbot():
    """Display a general farming chatbot on the page."""
    st.markdown("### 💬 Ask the Farming Assistant")
    st.markdown("*Have a question? Ask me anything about farming, crops, or how to use this tool!*")
    
    helper = FarmerHelperBot()
    
    if not helper.enabled:
        st.warning("⚠️ Chatbot requires Gemini API key. Please add your key to the `.env` file to enable chat features.")
        
        # Debug information
        env_path = Path(__file__).parent.parent.parent / '.env'
        api_key = os.getenv('GEMINI_API_KEY', '')
        
        with st.expander("🔧 Debug Information"):
            st.write(f"**.env file path:** `{env_path}`")
            st.write(f"**.env file exists:** {'✅ Yes' if env_path.exists() else '❌ No'}")
            st.write(f"**API key found:** {'✅ Yes' if api_key else '❌ No'}")
            if api_key:
                st.write(f"**API key length:** {len(api_key)} characters")
                st.write(f"**Starts with 'AIza':** {'✅ Yes' if api_key.startswith('AIza') else '❌ No'}")
        
        st.code("GEMINI_API_KEY=your_actual_api_key_here", language="bash")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
        st.warning("**Try refreshing the page (F5) after updating the .env file**")
        return
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"**🧑‍🌾 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {message['content']}")
    
    # Chat input
    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Your question:",
                placeholder="e.g., How do I improve wheat yield? What is nitrogen?",
                label_visibility="collapsed"
            )
        with col2:
            submit = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit and user_input.strip():
            # Check rate limits first
            if not helper._can_make_request():
                st.warning("⏳ **Rate Limit:** Please wait 15 seconds between questions.")
                st.info("💡 **Tip:** Ask detailed questions to get more complete answers!")
                return
                
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get AI response with rate limiting
            with st.spinner("🤔 Getting your answer..."):
                response = helper.chat_with_farmer(
                    user_input,
                    st.session_state.chat_history[:-1]  # Exclude current message
                )
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            # Rerun to show new messages
            st.rerun()
    
    # Show usage info
    if helper.enabled:
        remaining = max(0, helper.max_requests_per_minute - helper.request_count)
        if remaining <= 2:
            st.info(f"⏳ **Usage:** {remaining} questions remaining this minute")
    
    # Clear chat button
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
