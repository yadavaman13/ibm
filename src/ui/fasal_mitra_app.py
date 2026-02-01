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
col_title, col_support, col_lang = st.columns([2, 1, 1])

with col_title:
    app_title_display = get_text('app_title')
    st.markdown(f'<div class="app-title"><i class="ri-plant-fill"></i> {app_title_display}</div>', unsafe_allow_html=True)

with col_support:
    support_text = get_text('support')
    st.markdown(f'<div style="text-align: right; padding-top: 0.5rem; font-size: 0.95rem; color: #1B5E20;">{support_text}</div>', unsafe_allow_html=True)

with col_lang:
    # Render language selector
    language_service.render_language_selector("header")

# Hero heading - centered with multilingual support
hero_text = get_text('hero_welcome')
st.markdown(f'<div class="hero-heading">{hero_text}</div>', unsafe_allow_html=True)

# Enhanced search bar - centered with proper container
st.markdown('<div class="search-container">', unsafe_allow_html=True)

# Create columns for proper layout
search_col1, search_main_col, search_col2 = st.columns([0.5, 20, 0.5])

with search_main_col:
    # Container with search icon and input
    st.markdown('<div style="position: relative;">', unsafe_allow_html=True)
    st.markdown('<div class="search-icon-container"><i class="ri-search-line"></i></div>', unsafe_allow_html=True)
    
    search_placeholder = get_text('search_placeholder')
    search_query = st.text_input(
        "",
        placeholder=search_placeholder,
        key="search_input",
        label_visibility='collapsed'
    )
    
    st.markdown("""
    <div class="mic-container">
        <div class="mic-button">
            <i class="ri-mic-line"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
