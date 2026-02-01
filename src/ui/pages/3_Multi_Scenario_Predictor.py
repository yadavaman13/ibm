"""
Multi-Scenario Outcome Predictor Page
Compare multiple "what-if" farming scenarios
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import ML model components
from src.core.data_loader import DataLoader
from src.features.multi_scenario_predictor import MultiScenarioPredictor
from src.utils.language_service import get_language_service, get_text, get_current_language

# Initialize language service
language_service = get_language_service()
current_lang = get_current_language()

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

# Page configuration with language support
page_title = get_text('multi_scenario_predictor_title', 'en')
st.set_page_config(
    page_title=f"{page_title} - FasalMitra",
    page_icon="🎯",
    layout="wide"
)

# Page configuration
st.set_page_config(
    page_title="Multi-Scenario Predictor - FasalMitra",
    page_icon="🎯",
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
    
    .stMarkdown, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #1B5E20 !important;
    }
    
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
    
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stSelectbox > div > div {
        background-color: white !important;
    }
    
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
    
    .stNumberInput input[type="number"] {
        background-color: white !important;
        color: #1B5E20 !important;
        caret-color: #1B5E20 !important;
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
    
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: white !important;
    }
    
    /* Scenario card styling */
    .scenario-card {
        background: linear-gradient(135deg, #E8F5E9, #F1F8F4);
        border: 2px solid var(--secondary-green);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
        transition: all 0.3s ease;
    }
    
    .scenario-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
    }
    
    .scenario-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--primary-green);
        margin-bottom: 0.75rem;
    }
    
    .scenario-metric {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-dark);
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .risk-low {
        background-color: #C8E6C9;
        color: #2E7D32;
    }
    
    .risk-medium {
        background-color: #FFE082;
        color: #F57C00;
    }
    
    .risk-high {
        background-color: #FFCDD2;
        color: #D32F2F;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: white;
        border-left: 4px solid var(--secondary-green);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header with Back to Home button
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown("""
    <h2 style="color: var(--text-dark); margin-bottom: 1.5rem;">
        <i class="ri-target-line"></i> Multi-Scenario Outcome Predictor
    </h2>
    """, unsafe_allow_html=True)

with header_col2:
    if st.button("Back to Home", key="back_top"):
        st.switch_page("fasal_mitra_app.py")

# Initialize session state
if 'scenarios_generated' not in st.session_state:
    st.session_state.scenarios_generated = False

# Load data and initialize model
data_loader = load_agricultural_data()
scenario_predictor = initialize_predictor(data_loader) if data_loader else None

if data_loader is None or scenario_predictor is None:
    st.error("⚠️ Error loading agricultural data. Please check data files.")
    st.stop()

# Sidebar with language selector and navigation
with st.sidebar:
    language_settings_text = get_text('language_settings')
    st.markdown(f"### {language_settings_text}")
    language_service.render_language_selector("sidebar")
    
    # Add navigation
    st.markdown("---")
    home_text = get_text('go_to_home')
    if st.button(home_text, use_container_width=True):
        st.switch_page("src/ui/fasal_mitra_app.py")
    
    # Add some spacing
    st.markdown("---")

# Get current language for translations
current_lang = get_current_language()

# Page subtitles
page_subtitles = {
    'en': "*Explore multiple 'what-if' scenarios for your farming decisions and compare outcomes*",
    'hi': "*अपने कृषि निर्णयों के लिए कई 'क्या-अगर' परिदृश्यों का पता लगाएं और परिणामों की तुलना करें*",
    'mr': "*तुमच्या शेतीच्या निर्णयांसाठी अनेक 'काय-जर' परिस्थितींचा शोध घ्या आणि परिणामांची तुलना करा*",
    'gu': "*તમારા ખેતી નિર્ણયો માટે અનેક 'શું-જો' દૃશ્યો શોધો અને પરિણામોની સરખામણી કરો*",
    'pa': "*ਆਪਣੇ ਖੇਤੀ ਫੈਸਲਿਆਂ ਲਈ ਕਈ 'ਕੀ-ਜੇ' ਦ੍ਰਿਸ਼ਾਂ ਦੀ ਖੋਜ ਕਰੋ ਅਤੇ ਨਤੀਜਿਆਂ ਦੀ ਤੁਲਨਾ ਕਰੋ*",
    'bn': "*আপনার কৃষি সিদ্ধান্তের জন্য একাধিক 'কী-যদি' দৃশ্য অন্বেষণ করুন এবং ফলাফল তুলনা করুন*",
    'ta': "*உங்கள் விவசாய முடிவுகளுக்கான பல 'என்ன-என்றால்' காட்சிகளை ஆராய்ந்து முடிவுகளை ஒப்பிடவும்*",
    'te': "*మీ వ్యవసాయ నిర్ణయాలకు అనేక 'ఏమి-ఒకవేళ' దృశ్యాలను అన్వేషించండి మరియు ఫలితాలను పోల్చండి*",
    'kn': "*ನಿಮ್ಮ ಕೃಷಿ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ಅನೇಕ 'ಏನು-ಒಂದವೇಳೆ' ಸನ್ನಿವೇಶಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ಫಲಿತಾಂಶಗಳನ್ನು ಹೋಲಿಸಿ*",
    'ml': "*നിങ്ങളുടെ കൃഷി തീരുമാനങ്ങൾക്കായി ഒന്നിലധികം 'എന്താണ്-ഒരുപക്ഷേ' സാഹചര്യങ്ങൾ പര്യവേക്ഷണം ചെയ്ത് ഫലങ്ങൾ താരതമ്യം ചെയ്യുക*",
    'or': "*ଆପଣଙ୍କ କୃଷି ନିଷ୍ପତ୍ତି ପାଇଁ ଏକାଧିକ 'କଣ-ଯଦି' ଦୃଶ୍ୟ ଅନୁସନ୍ଧାନ କରନ୍ତୁ ଏବଂ ଫଳାଫଳ ତୁଳନା କରନ୍ତୁ*",
    'as': "*আপোনাৰ কৃষি সিদ্ধান্তৰ বাবে একাধিক 'কি-যদি' দৃশ্যপট অন্বেষণ কৰক আৰু ফলাফল তুলনা কৰক*"
}

st.markdown(page_subtitles.get(current_lang, page_subtitles['en']))
st.markdown("---")

# Input Form Section
section_headers = {
    'en': 'Base Configuration',
    'hi': 'आधार कॉन्फ़िगरेशन',
    'mr': 'मूळ कॉन्फिगरेशन',
    'gu': 'આધાર કોન્ફિગરેશન',
    'pa': 'ਬੇਸ ਕੰਨਫਿਗਰੇਸ਼ਨ',
    'bn': 'বেস কনফিগারেশন',
    'ta': 'அடிப்படை உள்ளமைவு',
    'te': 'బేస్ కన్ఫిగరేషన్',
    'kn': 'ಮೂಲ ಸಂರಚನೆ',
    'ml': 'ബേസ് കോൺഫിഗറേഷൻ',
    'or': 'ବେସ କନଫିଗରେସନ',
    'as': 'বেচ কনফিগাৰেচন'
}

st.markdown(f'<h3 style="color: var(--primary-green); margin-bottom: 1.5rem;"><i class="ri-settings-3-line"></i> {section_headers.get(current_lang, section_headers["en"])}</h3>', unsafe_allow_html=True)

# Get real data lists
available_states = ["Select State"] + data_loader.get_state_list()
available_crops = ["Select Crop"] + data_loader.get_crop_list()
available_seasons = ["Select Season"] + data_loader.get_season_list()

# Two-column input layout for basic parameters
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("**🌾 Crop Information**")
    crop = st.selectbox("Crop", available_crops, key="crop")
    state = st.selectbox("State", available_states, key="state")
    season = st.selectbox("Season", available_seasons, key="season")
    area = st.number_input("Farm Area (hectares)", min_value=0.1, value=1.0, step=0.5, format="%.1f", key="area")

with col2:
    st.markdown("**🧪 Input Management**")
    fertilizer = st.number_input("Fertilizer (kg/hectare)", min_value=0, value=25000, step=1000, format="%d", key="fertilizer")
    pesticide = st.number_input("Pesticide (kg/hectare)", min_value=0, value=500, step=50, format="%d", key="pesticide")

# Environmental & Soil conditions in 3-column layout
st.markdown('<h3 style="color: var(--primary-green); margin-top: 2rem; margin-bottom: 1rem;"><i class="ri-sun-cloudy-line"></i> Environmental & Soil Conditions</h3>', unsafe_allow_html=True)

env_col1, env_col2, env_col3 = st.columns(3, gap="small")

with env_col1:
    avg_temp = st.number_input("Temperature (°C)", min_value=10.0, max_value=45.0, value=25.0, step=0.5, format="%.1f", key="temp")
    rainfall = st.number_input("Rainfall (mm)", min_value=100, max_value=3000, value=1000, step=100, format="%d", key="rain")
    humidity = st.number_input("Humidity (%)", min_value=30, max_value=100, value=70, step=5, format="%d", key="humid")

with env_col2:
    pH = st.number_input("Soil pH", min_value=4.0, max_value=9.0, value=6.5, step=0.1, format="%.1f", key="ph")
    N = st.number_input("Nitrogen (N)", min_value=20, max_value=200, value=75, step=5, format="%d", key="n")

with env_col3:
    P = st.number_input("Phosphorus (P)", min_value=10, max_value=80, value=35, step=5, format="%d", key="p")
    K = st.number_input("Potassium (K)", min_value=10, max_value=60, value=30, step=5, format="%d", key="k")

# Generate Scenarios button - centered
st.markdown("<br>", unsafe_allow_html=True)
gen_col1, gen_col2, gen_col3 = st.columns([1, 1, 1])
with gen_col2:
    if st.button("🔮 Generate Scenarios", use_container_width=True, key="generate"):
        if (crop != "Select Crop" and state != "Select State" and season != "Select Season"):
            st.session_state.scenarios_generated = True
            st.session_state.base_params = {
                'crop': crop, 'state': state, 'season': season, 'area': area,
                'fertilizer': fertilizer, 'pesticide': pesticide, 'avg_temp_c': avg_temp,
                'total_rainfall_mm': rainfall, 'avg_humidity_percent': humidity,
                'pH': pH, 'N': N, 'P': P, 'K': K
            }
            st.rerun()
        else:
            st.error("⚠️ Please fill in all required fields (Crop, State, Season)")

st.markdown("---")

# Results Section
if st.session_state.scenarios_generated and 'base_params' in st.session_state:
    # Generate scenarios and predictions
    with st.spinner("🤖 Generating and analyzing multiple scenarios..."):
        base_params = st.session_state.base_params
        scenarios = scenario_predictor.create_scenarios(base_params)
        scenario_results = scenario_predictor.predict_scenarios(scenarios)
        comparison = scenario_predictor.compare_scenarios(scenario_results)
    
    if not scenario_results:
        st.error("Could not generate scenario predictions. Please try again.")
    else:
        # Display results
        st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1.5rem;"><i class="ri-bar-chart-box-line"></i> Scenario Analysis Results</h3>', unsafe_allow_html=True)
        
        # Scenario Comparison Table
        st.markdown("**📊 Scenario Comparison Table**")
        scenario_df = pd.DataFrame([
            {
                'Scenario': result['scenario_name'],
                'Type': result.get('scenario_type', 'N/A').replace('_', ' ').title(),
                'Predicted Yield (q/ha)': f"{result['predicted_yield']:.1f}",
                'Risk Level': result['risk_level'].title(),
                'Estimated Profit (₹)': f"{result['estimated_profit']['profit']:,.0f}",
                'Confidence Range': result['yield_range']
            }
            for result in scenario_results
        ])
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)
        
        # Yield vs Profit Chart
        st.markdown('<h3 style="color: var(--primary-green); margin-top: 2rem; margin-bottom: 1rem;"><i class="ri-line-chart-line"></i> Yield vs Profit Analysis</h3>', unsafe_allow_html=True)
        
        yields = [r['predicted_yield'] for r in scenario_results]
        profits = [r['estimated_profit']['profit'] for r in scenario_results]
        names = [r['scenario_name'] for r in scenario_results]
        colors = [{'low': '#2E7D32', 'medium': '#F57C00', 'high': '#D32F2F'}[r['risk_level']] for r in scenario_results]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=names, y=yields, name="Predicted Yield", marker_color=colors, opacity=0.7),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=names, y=profits, mode='lines+markers', name="Profit", 
                      line=dict(color='#1976D2', width=3), marker=dict(size=8)),
            secondary_y=True
        )
        
        fig.update_yaxes(title_text="Yield (quintal/ha)", secondary_y=False)
        fig.update_yaxes(title_text="Profit (₹)", secondary_y=True)
        fig.update_layout(
            title="Scenario Comparison: Yield vs Profit",
            height=450,
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk vs Return Scatter
        st.markdown('<h3 style="color: var(--primary-green); margin-top: 2rem; margin-bottom: 1rem;"><i class="ri-bubble-chart-line"></i> Risk vs Return Analysis</h3>', unsafe_allow_html=True)
        
        risk_mapping = {'low': 1, 'medium': 2, 'high': 3}
        risk_scores = [risk_mapping[r['risk_level']] for r in scenario_results]
        
        min_profit = min(profits)
        size_values = [abs(p - min_profit) + 1000 for p in profits]
        
        fig = px.scatter(
            x=risk_scores, y=yields, text=names, size=size_values,
            labels={'x': 'Risk Level (1=Low, 2=Medium, 3=High)', 'y': 'Expected Yield (quintal/ha)'},
            title="Risk vs Return Analysis",
            color=yields,
            color_continuous_scale='Greens'
        )
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=2, color='white')))
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Smart Recommendations - 3 column layout
        st.markdown('<h3 style="color: var(--primary-green); margin-top: 2rem; margin-bottom: 1rem;"><i class="ri-lightbulb-line"></i> Smart Recommendations</h3>', unsafe_allow_html=True)
        
        rec_col1, rec_col2, rec_col3 = st.columns(3, gap="medium")
        
        with rec_col1:
            best_yield = comparison['best_for_yield']
            st.markdown(f"""
            <div class="scenario-card" style="border-left: 4px solid #2E7D32;">
                <div class="scenario-title">🏆 Highest Yield</div>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 0.9rem; color: #666;">{best_yield['scenario']}</div>
                    <div class="scenario-metric" style="color: #2E7D32;">{best_yield['yield']:.1f} q/ha</div>
                    <div style="font-size: 0.85rem; color: #2E7D32; margin-top: 0.5rem;">
                        +{best_yield['improvement_over_baseline']:.1f} vs baseline
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_col2:
            best_profit = comparison['best_for_profit']
            st.markdown(f"""
            <div class="scenario-card" style="border-left: 4px solid #1976D2;">
                <div class="scenario-title">💰 Highest Profit</div>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 0.9rem; color: #666;">{best_profit['scenario']}</div>
                    <div class="scenario-metric" style="color: #1976D2;">₹{best_profit['profit']:,.0f}</div>
                    <div style="font-size: 0.85rem; color: #1976D2; margin-top: 0.5rem;">
                        +₹{best_profit['improvement_over_baseline']:,.0f} vs baseline
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_col3:
            lowest_risk = comparison['lowest_risk']
            st.markdown(f"""
            <div class="scenario-card" style="border-left: 4px solid #F57C00;">
                <div class="scenario-title">🛡️ Safest Option</div>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 0.9rem; color: #666;">{lowest_risk['scenario']}</div>
                    <div class="scenario-metric" style="color: #F57C00;">{lowest_risk['yield']:.1f} q/ha</div>
                    <div style="font-size: 0.85rem; color: #F57C00; margin-top: 0.5rem;">
                        Risk: {lowest_risk['risk_level'].title()}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Decision Guide
        st.markdown('<h3 style="color: var(--primary-green); margin-top: 2rem; margin-bottom: 1rem;"><i class="ri-guide-line"></i> Decision Guide</h3>', unsafe_allow_html=True)
        
        recommendations = comparison['recommendations']
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #666;">
        <i class="ri-bar-chart-box-line" style="font-size: 4rem; color: var(--light-green);"></i>
        <h3 style="color: var(--text-dark); margin-top: 1rem;">No Scenarios Generated Yet</h3>
        <p>Fill in your farming parameters and click "Generate Scenarios" to compare multiple strategies</p>
    </div>
    """, unsafe_allow_html=True)

