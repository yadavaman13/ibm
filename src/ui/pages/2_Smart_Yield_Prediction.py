"""
Smart Yield Prediction Page
AI-powered yield prediction with explanations
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import ML model components
from src.core.data_loader import DataLoader
from src.features.multi_scenario_predictor import MultiScenarioPredictor

# Initialize data and ML model
@st.cache_data
def load_agricultural_data():
    """Load and cache the agricultural datasets."""
    try:
        data_loader = DataLoader(str(project_root))
        data_loader.load_datasets()
        data_loader.merge_datasets()
        return data_loader
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def initialize_predictor(_data_loader):
    """Initialize and train the prediction model."""
    if _data_loader is None:
        return None
    try:
        predictor = MultiScenarioPredictor(_data_loader)
        predictor.train_prediction_model()
        return predictor
    except Exception as e:
        st.error(f"Error initializing predictor: {e}")
        return None

# Page configuration
st.set_page_config(
    page_title="Smart Yield Prediction - FasalMitra",
    page_icon="🌾",
    layout="wide"
)

# Include Remix Icons
st.markdown(
    '<link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">',
    unsafe_allow_html=True
)

# Custom CSS following established standards
st.markdown("""
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
        padding-top: 1rem !important;
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
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: white !important;
        color: #1B5E20 !important;
        border-radius: 8px !important;
        border: 2px solid #E8F5E9 !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--secondary-green) !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Force input containers to have white background */
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stSelectbox > div > div {
        background-color: white !important;
    }
    
    /* Force dropdown menu options to white */
    .stSelectbox div[role="listbox"] {
        background-color: white !important;
    }
    
    .stSelectbox div[role="option"] {
        background-color: white !important;
        color: #1B5E20 !important;
    }
    
    .stSelectbox div[role="option"]:hover {
        background-color: #F1F8F4 !important;
        color: var(--primary-green) !important;
    }
    
    /* Force select dropdown container */
    .stSelectbox div[data-baseweb="popover"] {
        background-color: white !important;
    }
    
    .stSelectbox ul {
        background-color: white !important;
    }
    
    .stSelectbox li {
        background-color: white !important;
        color: #1B5E20 !important;
    }
    
    .stSelectbox li:hover {
        background-color: #E8F5E9 !important;
    }
    
    /* Force number input internal elements to white */
    .stNumberInput input[type="number"] {
        background-color: white !important;
        color: #1B5E20 !important;
        caret-color: #1B5E20 !important;  /* Make cursor visible */
    }
    
    .stNumberInput > div {
        background-color: white !important;
    }
    
    .stNumberInput div[data-baseweb="input"] {
        background-color: white !important;
    }
    
    .stNumberInput div[data-baseweb="base-input"] {
        background-color: white !important;
    }
    
    /* Hide number input +/- buttons */
    .stNumberInput button {
        display: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--secondary-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-green) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25) !important;
    }
    
    /* Force button text to be white */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: white !important;
    }
    
    /* Result card styling */
    .result-card {
        background: linear-gradient(135deg, #E8F5E9, #F1F8F4);
        border: 2px solid var(--secondary-green);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15);
    }
    
    /* Metric card - uniform sizing for 3-column layout */
    .metric-card {
        background: linear-gradient(135deg, #E8F5E9, #F1F8F4);
        border: 2px solid var(--secondary-green);
        border-radius: 16px;
        padding: 1.5rem;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(46, 125, 50, 0.25);
    }
    
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-dark);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-green);
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .metric-unit {
        font-size: 0.95rem;
        color: #666;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .metric-footer {
        font-size: 0.8rem;
        color: #888;
        margin-top: auto;
    }
    
    .risk-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .risk-high { background-color: #D32F2F; }
    .risk-medium { background-color: #F57C00; }
    .risk-low { background-color: #2E7D32; }
    
    .result-value {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-green);
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-label {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Explanation section */
    .explanation-box {
        background: white;
        border-left: 4px solid var(--secondary-green);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .factor-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        background: #F1F8F4;
        border-radius: 8px;
    }
    
    .factor-icon {
        font-size: 1.5rem;
        color: var(--primary-green);
    }
</style>
""", unsafe_allow_html=True)

# Header with Back to Home button
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown("""
    <h2 style="color: var(--text-dark); margin-bottom: 1.5rem;">
        <i class="ri-seedling-line"></i> Smart Yield Prediction
    </h2>
    """, unsafe_allow_html=True)

with header_col2:
    if st.button("Back to Home", key="back_top"):
        st.switch_page("fasal_mitra_app.py")

# Initialize session state
if 'prediction_done' not in st.session_state:
    st.session_state.prediction_done = False

# Load data and initialize model
data_loader = load_agricultural_data()
scenario_predictor = initialize_predictor(data_loader) if data_loader else None

if data_loader is None or scenario_predictor is None:
    st.error("⚠️ Error loading agricultural data. Please check data files.")
    st.stop()

# Main content - Input Section
st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1.5rem;"><i class="ri-file-list-3-line"></i> Enter Crop Details</h3>', unsafe_allow_html=True)

# Get real data lists from the model
available_states = ["Select State"] + data_loader.get_state_list()
available_crops = ["Select Crop"] + data_loader.get_crop_list()
available_seasons = ["Select Season"] + data_loader.get_season_list()

# Two-column input layout
input_col1, input_col2 = st.columns([1, 1], gap="medium")

with input_col1:
    # Crop selection
    crop_type = st.selectbox(
        "🌱 Crop Type",
        available_crops,
        key="crop"
    )
    
    # Location inputs
    state = st.selectbox(
        "🗺️ State",
        available_states,
        key="state"
    )
    
    # Season
    season = st.selectbox(
        "📅 Season",
        available_seasons,
        key="season"
    )

with input_col2:
    # Farm size
    farm_size = st.number_input(
        "📏 Farm Size (hectares)",
        min_value=0.0,
        step=0.5,
        format="%.1f",
        value=1.0,
        key="farm_size"
    )
    
    # Fertilizer input
    fertilizer = st.number_input(
        "🧪 Fertilizer (kg/hectare)",
        min_value=0,
        step=1000,
        format="%d",
        value=25000,
        key="fertilizer"
    )
    
    # Soil pH
    ph = st.number_input(
        "🔬 Soil pH Level",
        min_value=4.0,
        max_value=9.0,
        step=0.1,
        format="%.1f",
        value=6.5,
        key="ph"
    )
    
    # Rainfall
    rainfall = st.number_input(
        "🌧️ Expected Rainfall (mm)",
        min_value=0,
        step=100,
        format="%d",
        value=1000,
        key="rainfall"
    )

# Predict button - centered below inputs
st.markdown("<br>", unsafe_allow_html=True)
predict_col1, predict_col2, predict_col3 = st.columns([1, 1, 1])
with predict_col2:
    if st.button("Predict Yield", use_container_width=True):
        if (state != "Select State" and crop_type != "Select Crop" and 
            season != "Select Season" and farm_size > 0):
            st.session_state.prediction_done = True
            st.session_state.user_inputs = {
                'crop': crop_type,
                'state': state,
                'season': season,
                'area': farm_size,
                'fertilizer': fertilizer,
                'pH': ph,
                'total_rainfall_mm': rainfall,
                'pesticide': 500,
                'avg_temp_c': 25,
                'avg_humidity_percent': 70,
                'N': 75,
                'P': 35,
                'K': 30,
                'scenario_name': 'Your Prediction',
                'scenario_type': 'user_input'
            }
            st.rerun()
        else:
            st.error("⚠️ Please fill in all required fields to get prediction")

st.markdown("---")

# Prediction Results Section
if st.session_state.prediction_done and 'user_inputs' in st.session_state:
    # Make real ML prediction
    with st.spinner("🤖 Making AI prediction..."):
        results = scenario_predictor.predict_scenarios([st.session_state.user_inputs])
    
    if not results:
        st.error("Could not generate prediction. Please try again.")
    else:
        prediction = results[0]
        user_crop = st.session_state.user_inputs['crop']
        user_state = st.session_state.user_inputs['state']
        user_season = st.session_state.user_inputs['season']
        user_area = st.session_state.user_inputs['area']
        
        # Main Result Cards - Three Column Layout
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1.5rem;"><i class="ri-bar-chart-box-line"></i> Predicted Yield</h3>', unsafe_allow_html=True)
        
        total_yield = prediction['predicted_yield'] * user_area
        risk_level = prediction['risk_level']
        risk_dot_class = {'low': 'risk-low', 'medium': 'risk-medium', 'high': 'risk-high'}
        
        # Three-column layout for metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
        
        with metric_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Predicted Yield per Hectare</div>
                <div class="metric-value">{prediction['predicted_yield']:.1f}</div>
                <div class="metric-unit">Quintals / Hectare</div>
                <div class="metric-footer">Range: {prediction['yield_range']} q/ha</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Expected Yield</div>
                <div class="metric-value">{total_yield:.1f}</div>
                <div class="metric-unit">Quintals from {user_area} Hectare{'s' if user_area != 1 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Risk Level</div>
                <div style="margin: 1.5rem 0;">
                    <span class="risk-indicator {risk_dot_class[risk_level]}"></span>
                    <span style="font-size: 1.8rem; font-weight: 700; color: var(--primary-green);">{risk_level.title()}</span>
                </div>
                <div class="metric-footer">Prediction confidence indicator</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Historical Context & Chart in 2-column layout
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 2rem;"><i class="ri-history-line"></i> Historical Context & Comparison</h3>', unsafe_allow_html=True)
        
        historical_data = data_loader.filter_data(crop=user_crop, state=user_state, season=user_season)
        
        # Initialize variables with defaults
        historical_max = 0
        historical_avg = 0
        historical_min = 0
        
        if not historical_data.empty:
            historical_avg = historical_data['yield'].mean()
            historical_max = historical_data['yield'].max()
            historical_min = historical_data['yield'].min()
            
            hist_col1, hist_col2 = st.columns([1, 1], gap="medium")
            
            with hist_col1:
                if prediction['predicted_yield'] > historical_avg:
                    comparison_text = f"✅ Your prediction is <strong>{prediction['predicted_yield'] - historical_avg:.1f} quintals/ha above</strong> regional average!"
                    comparison_color = "#2E7D32"
                else:
                    comparison_text = f"⚠️ Your prediction is <strong>{historical_avg - prediction['predicted_yield']:.1f} quintals/ha below</strong> regional average"
                    comparison_color = "#F57C00"
                
                st.markdown(f"""
                <div class="explanation-box" style="border-left-color: {comparison_color};">
                    <p style="margin-bottom: 1rem;">{comparison_text}</p>
                    <p><strong>Regional Performance ({user_crop} in {user_state}):</strong></p>
                    <ul>
                        <li>Average: {historical_avg:.1f} quintals/ha</li>
                        <li>Best ever: {historical_max:.1f} quintals/ha</li>
                        <li>Lowest: {historical_min:.1f} quintals/ha</li>
                        <li>Based on {len(historical_data)} historical records</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with hist_col2:
                # Yield Distribution Chart
                fig = px.histogram(
                    historical_data, x='yield',
                    title=f'Yield Distribution',
                    labels={'yield': 'Yield (quintals/ha)', 'count': 'Records'},
                    color_discrete_sequence=['#81C784']
                )
                
                # Add prediction line
                fig.add_vline(
                    x=prediction['predicted_yield'],
                    line_dash="dash", line_color="red", line_width=2,
                    annotation_text=f"Your: {prediction['predicted_yield']:.1f}",
                    annotation_position="top"
                )
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # AI Explanation - Keep concise
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 2rem;"><i class="ri-lightbulb-line"></i> AI Explanation</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
            <p><strong>How we made this prediction:</strong></p>
            <ul>
                <li>✅ Analyzed 24 years of agricultural data (1997-2020)</li>
                <li>✅ Trained on 19,689+ historical farm records</li>
                <li>✅ AI model validated for accuracy and reliability</li>
                <li>✅ Considered soil, weather, and farming practices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Factors Analysis - Grid Layout (3 columns)
        fertilizer_val = st.session_state.user_inputs['fertilizer']
        ph_val = st.session_state.user_inputs['pH']
        rainfall_val = st.session_state.user_inputs['total_rainfall_mm']
        
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 2rem;"><i class="ri-focus-line"></i> Key Factors Analysis</h3>', unsafe_allow_html=True)
        
        # Fertilizer analysis
        if fertilizer_val < 20000:
            fert_icon = "⚠️"
            fert_msg = f"You're using {fertilizer_val:,} kg/ha. Consider increasing for better yield"
            fert_color = "#F57C00"
        elif fertilizer_val > 40000:
            fert_icon = "⚠️"
            fert_msg = f"You're using {fertilizer_val:,} kg/ha. This might be excessive"
            fert_color = "#D32F2F"
        else:
            fert_icon = "✅"
            fert_msg = f"Your {fertilizer_val:,} kg/ha is in reasonable range"
            fert_color = "#2E7D32"
        
        # pH analysis
        if ph_val < 6.0:
            ph_icon = "⚠️"
            ph_msg = f"pH {ph_val:.1f} is acidic. Consider liming to improve soil conditions"
            ph_color = "#F57C00"
        elif ph_val > 8.0:
            ph_icon = "⚠️"
            ph_msg = f"pH {ph_val:.1f} is alkaline. Consider adding organic matter"
            ph_color = "#F57C00"
        else:
            ph_icon = "✅"
            ph_msg = f"pH {ph_val:.1f} is in optimal range for most crops"
            ph_color = "#2E7D32"
        
        # Rainfall analysis
        if rainfall_val < 500:
            rain_icon = "⚠️"
            rain_msg = f"{rainfall_val}mm might be insufficient. Ensure adequate irrigation"
            rain_color = "#F57C00"
        elif rainfall_val > 2000:
            rain_icon = "⚠️"
            rain_msg = f"{rainfall_val}mm is high. Monitor for waterlogging and diseases"
            rain_color = "#F57C00"
        else:
            rain_icon = "✅"
            rain_msg = f"{rainfall_val}mm is suitable for {user_crop}"
            rain_color = "#2E7D32"
        
        # Display factors in 3-column grid
        factor_col1, factor_col2, factor_col3 = st.columns(3, gap="small")
        
        with factor_col1:
            st.markdown(f"""
            <div class="factor-item" style="background: linear-gradient(135deg, {fert_color}15, transparent); height: 120px;">
                <div class="factor-icon">{fert_icon}</div>
                <div>
                    <strong>Fertilizer Usage</strong><br>
                    <span style="color: #666; font-size: 0.85rem;">{fert_msg}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="factor-item" style="height: 100px; margin-top: 0.5rem;">
                <div class="factor-icon"><i class="ri-map-pin-line"></i></div>
                <div>
                    <strong>Location: {user_state}</strong><br>
                    <span style="color: #666; font-size: 0.85rem;">Regional climate analyzed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with factor_col2:
            st.markdown(f"""
            <div class="factor-item" style="background: linear-gradient(135deg, {ph_color}15, transparent); height: 120px;">
                <div class="factor-icon">{ph_icon}</div>
                <div>
                    <strong>Soil pH Level</strong><br>
                    <span style="color: #666; font-size: 0.85rem;">{ph_msg}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="factor-item" style="height: 100px; margin-top: 0.5rem;">
                <div class="factor-icon"><i class="ri-calendar-line"></i></div>
                <div>
                    <strong>Season: {user_season}</strong><br>
                    <span style="color: #666; font-size: 0.85rem;">Seasonal variations factored in</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with factor_col3:
            st.markdown(f"""
            <div class="factor-item" style="background: linear-gradient(135deg, {rain_color}15, transparent); height: 120px;">
                <div class="factor-icon">{rain_icon}</div>
                <div>
                    <strong>Rainfall Conditions</strong><br>
                    <span style="color: #666; font-size: 0.85rem;">{rain_msg}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations in 2-column grid
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 2rem;"><i class="ri-plant-line"></i> Recommendations</h3>', unsafe_allow_html=True)
        
        rec_col1, rec_col2 = st.columns(2, gap="medium")
        
        with rec_col1:
            st.markdown("""
            <div class="explanation-box">
                <p><strong>🌱 Crop Management</strong></p>
                <ul>
                    <li>Use certified seeds (10-15% yield increase)</li>
                    <li>Follow crop calendar for all operations</li>
                    <li>Monitor soil health regularly</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="explanation-box" style="margin-top: 0.5rem;">
                <p><strong>🧪 Input Optimization</strong></p>
                <ul>
                    <li>Balance fertilizer application (soil testing)</li>
                    <li>Optimize water management by growth stage</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_col2:
            st.markdown("""
            <div class="explanation-box">
                <p><strong>🐛 Pest & Disease Control</strong></p>
                <ul>
                    <li>Integrated pest management</li>
                    <li>Regular field inspection</li>
                    <li>Timely intervention when needed</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Pro Tip - conditional on having historical data
            if historical_max > 0:
                st.markdown(f"""
                <div class="explanation-box" style="margin-top: 0.5rem; border-left-color: #2E7D32;">
                    <p><strong>💡 Pro Tip</strong></p>
                    <p>Top performers in {user_state} achieve <strong>{historical_max:.1f} quintals/ha</strong>. Study their practices!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="explanation-box" style="margin-top: 0.5rem; border-left-color: #2E7D32;">
                    <p><strong>💡 Pro Tip</strong></p>
                    <p>Connect with local agricultural extension officers for region-specific advice!</p>
                </div>
                """, unsafe_allow_html=True)
    
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #666;">
        <i class="ri-seedling-line" style="font-size: 4rem; color: var(--light-green);"></i>
        <h3 style="color: var(--text-dark); margin-top: 1rem;">No Prediction Yet</h3>
        <p>Fill in your crop details and click "Predict Yield" to get AI-powered yield prediction</p>
    </div>
        """, unsafe_allow_html=True)
