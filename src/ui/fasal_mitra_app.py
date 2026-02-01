"""
FasalMitra - Home Page
AI-Powered Farming Advisory System
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="FasalMitra - Farming Advisory System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern agri-tech theme
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
    }
    
    /* Override Streamlit's default padding */
    .stMainBlockContainer {
        padding: 1rem !important;
    }
    
    /* Remove extra bottom space */
    .block-container {
        padding-bottom: 1rem !important;
        min-height: auto !important;
    }
    
    /* Force light mode - prevent dark mode override */
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
    
    /* Force all dropdown menus and popovers */
    div[role="listbox"],
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    /* Force all list and menu items */
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
    
    /* Header styling */
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--primary-green);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Main heading */
    .main-heading {
        text-align: center;
        font-size: 2rem;
        font-weight: 500;
        color: var(--text-dark);
        margin: 3rem 0 2.5rem 0;
    }
    
    /* Functionality cards */
    .functionality-card {
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08);
    }
    
    .functionality-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(46, 125, 50, 0.15);
        border-color: var(--secondary-green);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-dark);
        line-height: 1.4;
    }
    
    /* Search section */
    .search-section {
        margin-top: 4rem;
        display: flex;
        justify-content: center;
        gap: 1rem;
        align-items: center;
    }
    
    .search-container {
        max-width: 600px;
        width: 100%;
    }
    
    /* Help section */
    .help-section {
        margin-top: 3rem;
        text-align: left;
        padding-left: 2rem;
    }
    
    .help-link {
        color: #E91E63;
        font-size: 1rem;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }
    
    .help-link:hover {
        text-decoration: underline;
    }
    
    /* Language selector */
    .language-selector {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        color: var(--text-dark);
    }
    
    /* Streamlit button override */
    .stButton > button {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        padding: 0;
    }
    
    /* Voice button */
    .voice-btn {
        background: var(--secondary-green);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .voice-btn:hover {
        background: var(--primary-green);
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Header section
col_title, col_lang = st.columns([3, 1])

with col_title:
    st.markdown('<div class="app-title"><i class="ri-plant-fill" style="color: var(--primary-green);"></i> FasalMitra</div>', unsafe_allow_html=True)

with col_lang:
    st.markdown('<div class="language-selector">Language / भाषा</div>', unsafe_allow_html=True)
    language = st.selectbox(
        "",
        options=['English', 'हिंदी (Hindi)', 'ગુજરાતી (Gujarati)', 'తెలుగు (Telugu)', 
                 'தமிழ் (Tamil)', 'ಕನ್ನಡ (Kannada)', 'मराठी (Marathi)', 'বাংলা (Bengali)', 
                 'ਪੰਜਾਬੀ (Punjabi)'],
        key='lang_selector',
        label_visibility='collapsed'
    )
    st.session_state.language = language

# Main heading
st.markdown('<h2 class="main-heading">Select the functionality you want</h2>', unsafe_allow_html=True)

# Functionality cards section
st.markdown("<br>", unsafe_allow_html=True)

# Custom CSS for clickable cards
st.markdown("""
<style>
    /* Make buttons fill the container */
    div[data-testid="column"] > div > div > div > button {
        width: 100%;
        height: 180px;
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 16px;
        padding: 0;
        margin: 0;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08);
        transition: all 0.3s ease;
    }
    
    div[data-testid="column"] > div > div > div > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(46, 125, 50, 0.15);
        border-color: var(--secondary-green);
        background: white;
    }
    
    div[data-testid="column"] > div > div > div > button > div {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    /* Remix Icon styling */
    .card-icon i {
        font-size: 3rem;
        color: var(--primary-green);
    }
    
    button i {
        font-size: 3rem;
        color: var(--primary-green);
        margin-bottom: 0.5rem;
    }
    
    .search-icon i {
        font-size: 2rem;
        color: var(--text-dark);
    }
    
    .voice-icon i {
        font-size: 1.5rem;
        color: white;
    }
    
    .help-icon i {
        font-size: 1.2rem;
        color: #E91E63;
    }
</style>
""", unsafe_allow_html=True)

# Additional CSS for button-based cards
st.markdown("""
<style>
    /* Style buttons to look like cards - with high specificity */
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button[kind="secondary"] > div,
    div[data-testid="column"] button[kind="secondary"] div[data-baseweb] {
        background: white !important;
        border: 2px solid #E8F5E9 !important;
        border-radius: 16px !important;
        padding: 2rem 1.5rem !important;
        height: 180px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08) !important;
        color: #1B5E20 !important;
    }
    
    div[data-testid="column"] button[kind="secondary"]:hover,
    div[data-testid="column"] button[kind="secondary"]:hover > div,
    div[data-testid="column"] button[kind="secondary"]:hover div[data-baseweb] {
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 24px rgba(46, 125, 50, 0.15) !important;
        border-color: #4CAF50 !important;
        background: white !important;
    }
    
    div[data-testid="column"] button[kind="secondary"] p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #1B5E20 !important;
        margin: 0 !important;
        line-height: 1.4 !important;
    }
    
    /* Icon styling inside buttons */
    div[data-testid="column"] button[kind="secondary"] i {
        font-size: 3rem !important;
        color: #2E7D32 !important;
        display: block !important;
        margin-bottom: 1rem !important;
    }
    
    /* Ensure button text is always dark green */
    div[data-testid="column"] button[kind="secondary"] *,
    div[data-testid="column"] button[kind="secondary"] span,
    div[data-testid="column"] button[kind="secondary"] div {
        color: #1B5E20 !important;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="large")

# Card 1: Yield Gap Analysis
with col1:
    if st.button('📊\n\n**Yield Gap Analysis**', key="yield_gap", help="Compare your yield with top performers", use_container_width=True):
        st.switch_page("pages/4_Yield_Gap_Analysis.py")

# Card 2: Multi-Scenario Predictor
with col2:
    if st.button('🎯\n\n**Multi-Scenario\nPredictor**', key="multi_scenario", help="Compare multiple farming scenarios", use_container_width=True):
        st.switch_page("pages/3_Multi_Scenario_Predictor.py")

# Card 3: Smart Yield Prediction  
with col3:
    if st.button('🌾\n\n**Smart Yield\nPrediction**', key="smart_yield", help="AI-powered yield prediction with explanations", use_container_width=True):
        st.switch_page("pages/2_Smart_Yield_Prediction.py")

# Card 4: Disease Detection
with col4:
    if st.button('🦠\n\n**Disease\nDetection**', key="disease_detection", help="AI-powered crop disease detection", use_container_width=True):
        st.switch_page("pages/1_Disease_Detection.py")

# Search section
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Fix column alignment for search row */
    div.row-widget.stHorizontal > div[data-testid="column"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Search icon container */
    .search-icon-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 48px;
        width: 100%;
    }
    
    .search-icon-container i {
        font-size: 2rem;
        color: var(--text-dark);
        line-height: 48px;
    }
    
    /* Remove default margins from text input wrapper */
    .stTextInput {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stTextInput > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Make search input same height as mic button */
    .stTextInput > div > div > input {
        height: 48px !important;
        border-radius: 24px !important;
        padding: 0 1.5rem !important;
        margin: 0 !important;
    }
    
    /* Mic button container alignment */
    .mic-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 48px;
        width: 100%;
    }
    
    /* Mic button styling */
    .mic-button {
        background: transparent !important;
        border: 2px solid var(--secondary-green) !important;
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        flex-shrink: 0 !important;
    }
    
    .mic-button:hover {
        background: var(--secondary-green) !important;
        transform: scale(1.05) !important;
    }
    
    .mic-button i {
        font-size: 1.5rem !important;
        color: var(--secondary-green) !important;
        line-height: 1 !important;
    }
    
    .mic-button:hover i {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

search_col_left, icon_col, search_col, mic_col, search_col_right = st.columns([2, 0.3, 6, 0.3, 2], gap="small")

with search_col_left:
    pass  # Empty padding column

with icon_col:
    st.markdown('<div class="search-icon-container"><i class="ri-search-line"></i></div>', unsafe_allow_html=True)

with search_col:
    search_query = st.text_input(
        "",
        placeholder="search your problem",
        key="search_input",
        label_visibility='collapsed'
    )

with mic_col:
    st.markdown("""
    <div class="mic-container">
        <div class="mic-button" onclick="alert('Voice search coming soon!')">
            <i class="ri-mic-line"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with search_col_right:
    pass  # Empty padding column

# Help section
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem;">
    <i class="ri-customer-service-2-line" style="color: #E91E63; font-size: 1rem;"></i>
    <span style="color: #E91E63; font-size: 1rem;">Need Help?</span>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #ddd;">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 0.5rem 0;">'
    '<i class="ri-plant-line" style="color: var(--primary-green);"></i> FasalMitra - Empowering Farmers with AI | '
    'Developed with ❤️ for Indian Agriculture'
    '</div>',
    unsafe_allow_html=True
)
