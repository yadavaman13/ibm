"""
FasalMitra - Home Page
AI-Powered Farming Advisory System with Comprehensive Language Support
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.features.weather_service import WeatherService
from src.utils.language_service import get_language_service, get_text, get_current_language

# Page configuration with multilingual support
app_title = get_text('app_title', 'en')  # Get title in English for page config
st.set_page_config(
    page_title=f"{app_title} - Farming Advisory System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for centered, balanced modern design
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/remixicon@4.9.0/fonts/remixicon.css" rel="stylesheet"/>
<style>
    /* Main theme colors */
    :root {
        --primary-green: #2E7D32;
        --secondary-green: #4CAF50;
        --light-green: #81C784;
        --bg-light: #F1F8F4;
        --text-dark: #1B5E20;
        --text-gray: #666666;
    }
    
    /* Override Streamlit's default padding for centered layout */
    .stMainBlockContainer {
        padding: 0.5rem 2rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    .block-container {
        padding: 0.5rem 0 !important;
        min-height: auto !important;
    }
    
    /* Force light mode */
    body {
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
    }
    
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div,
    .main,
    .block-container {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Force all text to be dark */
    .stMarkdown, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #1B5E20 !important;
    }
    
    /* Force all base-web components to light mode */
    div[data-baseweb] {
        background-color: white !important;
    }
    
    div[role="listbox"],
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    ul, li,
    div[role="option"],
    [role="option"] {
        background-color: white !important;
        color: #1B5E20 !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Compact header */
    .app-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-green);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .language-selector {
        font-size: 0.9rem;
        color: var(--text-gray);
    }
    
    /* Hero section - centered */
    .hero-heading {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 500;
        color: var(--text-dark);
        margin: 1.5rem 0 1rem 0;
        line-height: 1.4;
    }
    
    /* Enhanced search bar */
    .search-container {
        width: 60%;
        margin: 1.5rem auto;
        position: relative;
    }
    
    .stTextInput > div > div > input {
        height: 56px !important;
        border-radius: 10px !important;
        padding: 0 4rem 0 3.5rem !important;
        border: 2px solid #E0E0E0 !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--secondary-green) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15) !important;
        outline: none !important;
    }
    
    /* Weather section - single unified card */
    .weather-section {
        margin: 1.5rem auto 2rem auto;
    }
    
    .weather-unified {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        height: 100px;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .weather-info-left {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 0.3rem;
    }
    
    .weather-location {
        font-size: 0.8rem;
        color: #546E7A;
        font-weight: 500;
    }
    
    .weather-datetime {
        font-size: 0.75rem;
        color: #546E7A;
    }
    
    .weather-current {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding-left: 1.5rem;
        border-left: 2px solid rgba(25, 118, 210, 0.2);
    }
    
    .current-temp {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1976D2;
        line-height: 1;
    }
    
    .weather-condition {
        font-size: 0.9rem;
        color: #37474F;
        white-space: nowrap;
    }
    
    .weather-forecast-section {
        display: flex;
        gap: 2rem;
        align-items: center;
        margin-left: auto;
        padding-left: 2rem;
        border-left: 2px solid rgba(25, 118, 210, 0.2);
    }
    
    .forecast-day-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
    }
    
    .forecast-day-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1B5E20;
    }
    
    .forecast-icon {
        font-size: 1.5rem;
    }
    
    .forecast-temps {
        font-size: 0.85rem;
        color: #1976D2;
        font-weight: 600;
    }
    
    /* Section heading - centered */
    .section-heading {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 2rem 0 1.5rem 0;
    }
    
    /* Cards container - centered */
    .cards-container {
        max-width: 1200px;
        margin: 0 auto 2rem auto;
    }
    
    /* Streamlit button styling for cards */
    .stButton > button {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        padding: 0;
    }
    
    /* Feature card styling */
    .feature-card {
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 14px;
        padding: 1.5rem 1rem;
        text-align: center;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.15);
        border-color: var(--secondary-green);
    }
    
    .card-icon {
        font-size: 3rem;
        color: var(--primary-green);
        margin-bottom: 0.5rem;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-dark);
        line-height: 1.3;
    }
    
    /* Search icon positioning */
    .search-icon-container {
        position: absolute;
        left: 1.2rem;
        top: 50%;
        transform: translateY(-50%);
        z-index: 10;
        pointer-events: none;
    }
    
    .search-icon-container i {
        font-size: 1.3rem;
        color: var(--text-gray);
    }
    
    /* Mic button */
    .mic-container {
        position: absolute;
        right: 0.7rem;
        top: 50%;
        transform: translateY(-50%);
        z-index: 10;
    }
    
    .mic-button {
        background: white !important;
        border: 2px solid var(--secondary-green) !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .mic-button:hover {
        background: var(--secondary-green) !important;
        transform: scale(1.05) !important;
    }
    
    .mic-button i {
        font-size: 1.1rem !important;
        color: var(--secondary-green) !important;
    }
    
    .mic-button:hover i {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for language support
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False

# Initialize language service
language_service = get_language_service()
current_lang = get_current_language()

# Initialize weather service
@st.cache_resource
def get_weather_service():
    """Initialize and cache weather service"""
    return WeatherService()

weather_service = get_weather_service()

# Fetch weather data for default location (New Delhi)
if st.session_state.weather_data is None:
    try:
        # Default location: New Delhi
        weather_data = weather_service.get_complete_weather(28.6139, 77.2090, forecast_days=3)
        # Check if there's an error in the response
        if weather_data and not weather_data.get('error'):
            st.session_state.weather_data = weather_data
        else:
            st.session_state.weather_data = {'error': 'Unable to fetch weather'}
    except Exception as e:
        # Initialize with empty dict on error
        st.session_state.weather_data = {'error': str(e)}

# Compact header section with language support
col_title, col_lang = st.columns([3, 1])

with col_title:
    app_title_display = get_text('app_title')
    st.markdown(f'<div class="app-title"><i class="ri-plant-fill"></i> {app_title_display}</div>', unsafe_allow_html=True)

with col_lang:
    # Render language selector
    language_service.render_language_selector("header")

# Hero heading - centered with multilingual support
hero_text = get_text('hero_welcome')
st.markdown(f'<div class="hero-heading">{hero_text}</div>', unsafe_allow_html=True)

# Weather section - single unified card
weather_data = st.session_state.weather_data

if weather_data and not weather_data.get('error'):
    current = weather_data.get('current', {})
    forecast = weather_data.get('forecast', [])
    
    # Get current date/time
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p IST")
    
    # Build unified weather card HTML
    weather_html = f"""<div class="weather-section">
<div class="weather-unified">
<div class="weather-info-left">
<div class="weather-location">📍 New Delhi, Delhi</div>
<div class="weather-datetime">{date_str} • {time_str}</div>
</div>
<div class="weather-current">
<div class="current-temp">{current.get('temperature', 0):.0f}°C</div>
<div class="weather-condition">{weather_service.get_weather_emoji(current.get('weather_code', 0))} {current.get('weather_description', 'N/A')}</div>
</div>
<div class="weather-forecast-section">"""
    
    # Add forecast days (skip today, show next 2 days)
    if forecast and len(forecast) > 1:
        for day_forecast in forecast[1:3]:  # Show 2 days only
            date_obj = datetime.strptime(day_forecast['date'], '%Y-%m-%d')
            day_name = date_obj.strftime('%a')
            temp_min = day_forecast.get('temp_min', 0)
            temp_max = day_forecast.get('temp_max', 0)
            emoji = weather_service.get_weather_emoji(day_forecast.get('weather_code', 0))
            
            weather_html += f"""<div class="forecast-day-item">
<div class="forecast-day-name">{day_name}</div>
<div class="forecast-icon">{emoji}</div>
<div class="forecast-temps">{temp_max:.0f}°/{temp_min:.0f}°</div>
</div>"""
    
    weather_html += """</div>
</div>
</div>"""
    
    st.markdown(weather_html, unsafe_allow_html=True)

# Section heading - centered with multilingual support
section_title = get_text('explore_solutions')
st.markdown(f'<div class="section-heading">{section_title}</div>', unsafe_allow_html=True)

# Feature cards - centered container with equal width columns
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

# Card 1: Multi-Scenario Predictor
with col1:
    card_title_1 = get_text('multi_scenario_predictor')
    st.markdown(f"""
    <div class="feature-card">
        <i class="ri-git-branch-line card-icon"></i>
        <div class="card-title">{card_title_1}</div>
    </div>
    """, unsafe_allow_html=True)
    open_text = get_text('open_button')
    if st.button(open_text, key="open_multi_scenario", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Multi_Scenario_Predictor.py")

# Card 2: Smart Yield Prediction
with col2:
    card_title_2 = get_text('smart_yield_prediction')
    st.markdown(f"""
    <div class="feature-card">
        <i class="ri-seedling-line card-icon"></i>
        <div class="card-title">{card_title_2}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(open_text, key="open_smart_yield", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Smart_Yield_Prediction.py")

# Card 3: Disease Detection
with col3:
    card_title_3 = get_text('disease_detection')
    st.markdown(f"""
    <div class="feature-card">
        <i class="ri-search-eye-line card-icon"></i>
        <div class="card-title">{card_title_3}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(open_text, key="open_disease", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Disease_Detection.py")

# Card 4: Yield Gap Analysis
with col4:
    card_title_4 = get_text('yield_gap_analysis')
    st.markdown(f"""
    <div class="feature-card">
        <i class="ri-bar-chart-grouped-line card-icon"></i>
        <div class="card-title">{card_title_4}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(open_text, key="open_yield_gap", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Yield_Gap_Analysis.py")

st.markdown('</div>', unsafe_allow_html=True)  # Close cards-container

# ==================== INTELLIGENT SEARCH ASSISTANT ====================
st.markdown("---")

# Import chatbot
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.farmer_helper_bot import FarmerHelperBot

# Initialize chatbot
if 'farming_assistant' not in st.session_state:
    st.session_state.farming_assistant = FarmerHelperBot()
    st.session_state.search_history = []
    st.session_state.assistant_chat = []

helper = st.session_state.farming_assistant

# Header
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="color: #2E7D32; margin-bottom: 0.5rem;">🔍 Intelligent Farming Assistant</h2>
    <p style="color: #666; font-size: 1.1rem;">Ask any farming question or search for features - I'll guide you!</p>
</div>
""", unsafe_allow_html=True)

# Feature mapping for intelligent suggestions
feature_keywords = {
    'disease': {
        'keywords': ['disease', 'sick', 'pest', 'infection', 'leaf', 'spot', 'fungus', 'bacteria', 'virus', 'blight', 'rust', 'mildew', 'treatment', 'cure', 'diagnose', 'identify'],
        'feature': 'Disease Detection',
        'page': 'pages/1_Disease_Detection.py',
        'description': '🔬 Upload crop photos to detect diseases and get treatment recommendations',
        'icon': '🔬'
    },
    'yield': {
        'keywords': ['yield', 'production', 'output', 'harvest', 'how much', 'quintal', 'ton', 'predict', 'forecast', 'estimate'],
        'feature': 'Yield Prediction',
        'page': 'pages/2_Smart_Yield_Prediction.py',
        'description': '🌾 Predict your crop yield with 97% accuracy using AI',
        'icon': '🌾'
    },
    'scenario': {
        'keywords': ['scenario', 'what if', 'compare', 'different', 'options', 'alternative', 'strategy', 'fertilizer amount', 'season change'],
        'feature': 'Multi-Scenario Analysis',
        'page': 'pages/3_Multi_Scenario_Predictor.py',
        'description': '🎯 Compare different farming strategies and see potential outcomes',
        'icon': '🎯'
    },
    'gap': {
        'keywords': ['gap', 'improve', 'better', 'increase', 'optimize', 'potential', 'maximum', 'best', 'performance'],
        'feature': 'Yield Gap Analysis',
        'page': 'pages/4_Yield_Gap_Analysis.py',
        'description': '📊 Discover how to close the gap between actual and potential yields',
        'icon': '📊'
    },
    'weather': {
        'keywords': ['weather', 'rain', 'temperature', 'forecast', 'climate', 'humidity', 'wind', 'sunny', 'cloudy'],
        'feature': 'Weather Forecast',
        'page': 'pages/5_Weather_Forecast.py',
        'description': '🌤️ Get 7-day weather predictions for better crop planning',
        'icon': '🌤️'
    }
}

def analyze_query_intent(query):
    """Analyze user query and suggest relevant features."""
    query_lower = query.lower()
    suggestions = []
    
    for category, data in feature_keywords.items():
        for keyword in data['keywords']:
            if keyword in query_lower:
                if data not in suggestions:
                    suggestions.append(data)
                break
    
    return suggestions

# Search input with enhanced styling
st.markdown("""
<style>
.search-assistant-section {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-top: 2rem;
}
.smart-search-container {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}
.chat-message-user {
    background: #E3F2FD;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1rem 0;
    border-left: 4px solid #2196F3;
    box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}
.chat-message-bot {
    background: #F1F8E9;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 2px solid #4CAF50;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
    position: relative;
}
.chat-message-bot::before {
    content: '';
    position: absolute;
    left: -2px;
    top: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    border-radius: 12px;
    z-index: -1;
    opacity: 0.1;
}
.ai-response-header {
    color: #2E7D32;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #E8F5E9;
}
.feature-suggestion-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #2196F3;
    margin: 0.8rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
}
.feature-suggestion-card:hover {
    box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Search form
with st.form(key='intelligent_search_form', clear_on_submit=True):
    col_search, col_btn = st.columns([5, 1])
    
    with col_search:
        search_query = st.text_input(
            "Search or Ask",
            placeholder="e.g., How to detect wheat diseases? What will be my rice yield? Best time to plant tomatoes?",
            label_visibility="collapsed",
            key="smart_search_input"
        )
    
    with col_btn:
        search_submit = st.form_submit_button("🔍 Search", use_container_width=True, type="primary")

# Process search query
if search_submit and search_query.strip():
    # Add to history
    st.session_state.search_history.append(search_query)
    
    # Analyze intent
    suggestions = analyze_query_intent(search_query)
    
    # Show AI response
    st.markdown('<div class="ai-response-header">🤖 AI Assistant Response</div>', unsafe_allow_html=True)
    
    if helper.enabled:
        if helper._can_make_request():
            with st.spinner("🧠 Analyzing your question..."):
                # Enhanced prompt for better responses
                enhanced_query = f"""
User Question: {search_query}

You are FasalMitra's AI assistant. Provide:
1. Direct answer to the question (2-3 sentences)
2. Practical farming advice
3. If relevant, mention which FasalMitra features can help (Disease Detection, Yield Prediction, Weather Forecast, Multi-Scenario Analysis, Yield Gap Analysis)

Keep it friendly, simple, and actionable for farmers.
"""
                response = helper.chat_with_farmer(enhanced_query, st.session_state.assistant_chat[-4:])
                
                st.session_state.assistant_chat.append({'role': 'user', 'content': search_query})
                st.session_state.assistant_chat.append({'role': 'assistant', 'content': response})
                
                st.markdown(f'<div class="chat-message-bot"><div style="font-size: 1.1rem; margin-bottom: 0.8rem;">💬 <strong style="color: #2E7D32;">FasalMitra Assistant</strong></div><div style="line-height: 1.6; color: #333;">{response}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("⏳ Please wait 15 seconds between questions to avoid rate limits.")
    else:
        st.info("🤖 AI features require Gemini API key. Showing feature suggestions below.")
    
    # Show feature suggestions
    if suggestions:
        st.markdown('<div class="ai-response-header" style="margin-top: 2rem;">🎯 Recommended Features for Your Query</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #666; margin-bottom: 1.5rem; font-size: 1.05rem;'>Based on your question, these features can help you:</p>", unsafe_allow_html=True)
        
        for idx, suggestion in enumerate(suggestions):
            st.markdown('<div class="feature-suggestion-card">', unsafe_allow_html=True)
            col_icon, col_content, col_action = st.columns([1, 5, 2])
            
            with col_icon:
                st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{suggestion['icon']}</div>", unsafe_allow_html=True)
            
            with col_content:
                st.markdown(f"<div style='font-size: 1.2rem; font-weight: 600; color: #1976D2; margin-bottom: 0.3rem;'>{suggestion['feature']}</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #555; font-size: 0.95rem; margin: 0;'>{suggestion['description']}</p>", unsafe_allow_html=True)
            
            with col_action:
                if st.button(f"Open {suggestion['icon']}", key=f"nav_{idx}_{suggestion['feature'].replace(' ', '_')}", use_container_width=True, type="primary"):
                    st.switch_page(suggestion['page'])
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # General suggestions when no specific match
        st.markdown("### 🌟 Explore Our Features")
        st.info("Not sure where to start? Check out all our farming tools above!")

# Show recent searches
if st.session_state.search_history:
    with st.expander("📜 Recent Searches", expanded=False):
        for i, search in enumerate(reversed(st.session_state.search_history[-5:])):
            st.markdown(f"{i+1}. {search}")

# Chat history
if st.session_state.assistant_chat:
    with st.expander("💬 Conversation History", expanded=False):
        for msg in st.session_state.assistant_chat[-10:]:
            if msg['role'] == 'user':
                st.markdown(f'<div class="chat-message-user">🧑‍🌾 <strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message-bot">🤖 <strong>Assistant:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", key="clear_assistant_history"):
            st.session_state.assistant_chat = []
            st.session_state.search_history = []
            st.rerun()

