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

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class FarmerHelperBot:
    """AI-powered helper bot to explain farming terminology to farmers."""
    
    def __init__(self):
        """Initialize the helper bot with Gemini API."""
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        if self.api_key and self.api_key != 'your_gemini_api_key_here':
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.enabled = True
        else:
            self.enabled = False
    
    def get_term_explanation(self, term, context="farming"):
        """
        Get explanation for a technical farming term.
        
        Args:
            term: The technical term to explain
            context: Additional context about where this term is used
            
        Returns:
            Dictionary with explanation, measurement methods, and resources
        """
        if not self.enabled:
            return self._get_fallback_explanation(term)
        
        try:
            prompt = f"""You are a helpful farming assistant explaining technical terms to farmers in simple language.

Explain the following farming term: "{term}"
Context: {context}

Provide your response in this exact JSON format:
{{
    "simple_explanation": "A simple, easy-to-understand explanation in 2-3 sentences",
    "why_important": "Why this matters for farming in 1-2 sentences",
    "how_to_measure": "Step-by-step guide on how a farmer can measure or determine this (3-5 practical steps)",
    "typical_values": "What are typical good/normal values for this?",
    "video_search": "Suggested YouTube search query to learn more",
    "tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Make it very practical and farmer-friendly. Use simple words, avoid jargon."""

            response = self.model.generate_content(prompt)
            
            import json
            # Extract JSON from response
            result_text = response.text
            # Try to find JSON in the response
            if '{' in result_text and '}' in result_text:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                json_str = result_text[start:end]
                result = json.loads(json_str)
            else:
                # Fallback if no JSON found
                result = self._get_fallback_explanation(term)
            
            return result
            
        except Exception as e:
            return self._get_fallback_explanation(term, str(e))
    
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
        General farming chatbot conversation.
        
        Args:
            user_question: Farmer's question
            conversation_history: List of previous messages
            
        Returns:
            AI response as a string
        """
        if not self.enabled:
            return "Sorry, chatbot is not available. Please add your Gemini API key to the .env file to enable this feature."
        
        try:
            # Build conversation context
            context = """You are a helpful farming assistant for Indian farmers. 
Speak in simple, easy-to-understand language. Be practical and give actionable advice.
If asked about technical terms, explain them simply. 
When relevant, suggest YouTube search terms or local resources like Krishi Vigyan Kendra.
Be encouraging and supportive. Remember that farmers may not have advanced education but are experienced in their work.

"""
            
            if conversation_history:
                for msg in conversation_history:
                    if msg['role'] == 'user':
                        context += f"Farmer: {msg['content']}\n"
                    else:
                        context += f"Assistant: {msg['content']}\n"
            
            context += f"Farmer: {user_question}\nAssistant:"
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            return f"Sorry, I couldn't process your question right now. Error: {str(e)}"


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
        st.code("GEMINI_API_KEY=your_actual_api_key_here", language="bash")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
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
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get AI response
            with st.spinner("🤔 Thinking..."):
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
    
    # Clear chat button
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
