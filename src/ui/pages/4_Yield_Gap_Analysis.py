"""
Yield Gap Analysis Page
Compare your farm's yield with top performers in your region
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_loader import DataLoader
from src.features.yield_gap_analyzer import YieldGapAnalyzer
from src.utils.language_service import get_language_service, get_text, get_current_language

# Initialize language service
language_service = get_language_service()
current_lang = get_current_language()

@st.cache_data
def load_agricultural_data():
    """Load and cache agricultural data"""
    # Get project root (4 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    data_loader = DataLoader(data_dir="dummy")  # Use non-".." to trigger else branch
    data_loader.data_dir = project_root  # Directly set the correct path
    return data_loader

@st.cache_resource
def initialize_analyzer(_data_loader):
    """Initialize and cache the yield gap analyzer"""
    return YieldGapAnalyzer(_data_loader)

# Page configuration with language support
page_title = get_text('yield_gap_analysis_title', 'en')
st.set_page_config(
    page_title=f"{page_title} - FasalMitra",
    page_icon="📊",
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
    
    /* Header styling */
    .page-header {
        background: linear-gradient(135deg, var(--primary-green), var(--secondary-green));
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15);
    }
    
    .page-header h1 {
        margin: 0;
        font-size: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .page-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08);
        margin-bottom: 1rem;
    }
    
    .info-card h3 {
        color: var(--primary-green);
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
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
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #F1F8F4, #E8F5E9);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        border: 2px solid var(--light-green);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-green);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress bar custom styling */
    .custom-progress {
        background: #E8F5E9;
        border-radius: 8px;
        height: 24px;
        position: relative;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .custom-progress-bar {
        background: linear-gradient(90deg, var(--primary-green), var(--secondary-green));
        height: 100%;
        border-radius: 8px;
        transition: width 0.6s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 0.5rem;
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with Back to Home button
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown("""
    <h2 style="color: var(--text-dark); margin-bottom: 1.5rem;">
        <i class="ri-bar-chart-line"></i> Yield Gap Analysis
    </h2>
    """, unsafe_allow_html=True)

with header_col2:
    if st.button("Back to Home", key="back_top"):
        st.switch_page("fasal_mitra_app.py")

# Initialize data and analyzer
try:
    data_loader = load_agricultural_data()
    analyzer = initialize_analyzer(data_loader)
    
    # Load datasets if not already loaded
    if data_loader.merged_data is None:
        data_loader.merge_datasets()
    
    available_crops = data_loader.get_crop_list()
    available_states = data_loader.get_state_list()
    available_seasons = data_loader.get_season_list()
except Exception as e:
    st.error(f"Error loading data: {e}")
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

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Input Form Section with translations
current_lang = get_current_language()

farm_details_headers = {
    'en': 'Farm Details',
    'hi': 'खेत का विवरण',
    'mr': 'शेताचा तपशील',
    'gu': 'ફાર્મની વિગતો',
    'pa': 'ਖੇਤ ਦਾ ਵੇਰਵਾ',
    'bn': 'খামারের বিবরণ',
    'ta': 'பண்ணை விவரங்கள்',
    'te': 'పొలం వివరాలు',
    'kn': 'ಫಾರ್ಮ್ ವಿವರಗಳು',
    'ml': 'ഫാം വിവരങ്ങൾ',
    'or': 'ଚାଷ ବିବରଣୀ',
    'as': 'ফাৰ্মৰ বিৱৰণ'
}

st.markdown(f'<h3 style="color: var(--primary-green); margin-bottom: 1rem;"><i class="ri-file-list-3-line"></i> {farm_details_headers.get(current_lang, farm_details_headers["en"])}</h3>', unsafe_allow_html=True)

# Two-column input layout
input_col1, input_col2 = st.columns(2, gap="medium")

with input_col1:
    # Farm location
    state = st.selectbox(
        "State",
        ["Select State"] + available_states,
        key="state"
    )
    
    # Crop selection
    crop_type = st.selectbox(
        "Crop Type",
        ["Select Crop"] + available_crops,
        key="crop"
    )
    
    # Season selection
    season = st.selectbox(
        "Season",
        ["All Seasons"] + available_seasons,
        key="season"
    )

with input_col2:
    # Farm details
    farm_size = st.number_input(
        "Farm Size (hectares)",
        min_value=0.0,
        step=0.5,
        format="%.1f",
        key="farm_size"
    )
    
    current_yield = st.number_input(
        "Your Current Yield (quintals/hectare)",
        min_value=0.0,
        step=0.5,
        format="%.1f",
        key="current_yield",
        help="Enter your average yield from recent harvests"
    )

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
with analyze_col2:
    if st.button("🔍 Analyze Yield Gap", use_container_width=True, type="primary"):
        if state != "Select State" and crop_type != "Select Crop" and farm_size > 0 and current_yield > 0:
            st.session_state.analysis_done = True
            st.rerun()
        else:
            st.error("⚠️ Please fill in all required fields to perform analysis")

st.markdown("<br>", unsafe_allow_html=True)

# Results Section
if st.session_state.analysis_done:
    # Validate current yield
    if st.session_state.current_yield <= 0:
        st.error("⚠️ Current yield must be greater than 0 to perform analysis")
    else:
        # Perform real yield gap analysis
        selected_season = None if st.session_state.season == "All Seasons" else st.session_state.season
        
        with st.spinner("Analyzing yield gap against historical data..."):
            gap_analysis = analyzer.analyze_user_gap(
                user_yield=st.session_state.current_yield,
                crop=st.session_state.crop,
                state=st.session_state.state,
                season=selected_season
            )
        
        # Check for errors
        if 'error' in gap_analysis:
            st.error(f"⚠️ {gap_analysis['error']}")
            if 'available_seasons' in gap_analysis and gap_analysis['available_seasons']:
                st.info(f"Available seasons for {st.session_state.crop} in {st.session_state.state}: {', '.join(gap_analysis['available_seasons'])}")
        else:
            benchmarks = gap_analysis['benchmarks']
            gaps = gap_analysis['gaps']
            percentile_rank = gap_analysis['percentile_rank']
            improvement_potential = gap_analysis['improvement_potential']
            recommendations = gap_analysis['recommendations']
            
            # Performance Metrics Section
            st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem;"><i class="ri-trophy-line"></i> Performance Analysis</h3>', unsafe_allow_html=True)
            
            # Key Metrics in 3 columns
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Your Yield</div>
                    <div class="metric-value">{st.session_state.current_yield:.1f}</div>
                    <div class="metric-label">quintals/hectare</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Top 10% Avg</div>
                    <div class="metric-value">{benchmarks['top_10_percent']:.1f}</div>
                    <div class="metric-label">quintals/hectare</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Your Percentile</div>
                    <div class="metric-value">{percentile_rank:.0f}%</div>
                    <div class="metric-label">rank</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Yield Distribution Chart
            st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 1.5rem;"><i class="ri-bar-chart-box-line"></i> Yield Distribution</h3>', unsafe_allow_html=True)
            
            # Get visualization data
            viz_data = analyzer.generate_visualization_data(
                user_yield=st.session_state.current_yield,
                crop=st.session_state.crop,
                state=st.session_state.state,
                season=selected_season
            )
            
            # Create histogram with benchmark lines
            fig = go.Figure()
            
            # Histogram of all yields
            fig.add_trace(go.Histogram(
                x=viz_data['yield_distribution'],
                name='Yield Distribution',
                marker_color='#81C784',
                opacity=0.7,
                nbinsx=30
            ))
            
            # Add vertical lines for benchmarks
            fig.add_vline(x=st.session_state.current_yield, line_dash="dash", 
                         line_color="#FF6B6B", annotation_text="Your Yield",
                         annotation_position="top")
            fig.add_vline(x=benchmarks['average_yield'], line_dash="dot", 
                         line_color="#4ECDC4", annotation_text="Average")
            fig.add_vline(x=benchmarks['top_10_percent'], line_dash="solid", 
                         line_color="#2E7D32", annotation_text="Top 10%",
                         annotation_position="top right")
            
            fig.update_layout(
                xaxis_title="Yield (quintals/hectare)",
                yaxis_title="Frequency",
                showlegend=False,
                height=350,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvement Potential Cards
            st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 1.5rem;"><i class="ri-rocket-line"></i> Improvement Potential</h3>', unsafe_allow_html=True)
            
            pot_col1, pot_col2, pot_col3 = st.columns(3)
            
            with pot_col1:
                conservative = improvement_potential['conservative']
                gain_quintals = conservative['improvement'] * st.session_state.farm_size
                st.markdown(f"""
                <div class="info-card" style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-color: #81C784;">
                    <h4 style="color: var(--primary-green); margin-top: 0;">🎯 Conservative</h4>
                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--primary-green); margin: 0.5rem 0;">
                        +{conservative['improvement']:.1f}
                    </p>
                    <p style="color: #666; margin: 0;">quintals/hectare</p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">Total gain: <strong>{gain_quintals:.0f} quintals</strong></p>
                    <p style="font-size: 0.85rem; color: #666;">{conservative['achievability']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with pot_col2:
                moderate = improvement_potential['moderate']
                gain_quintals = moderate['improvement'] * st.session_state.farm_size
                st.markdown(f"""
                <div class="info-card" style="background: linear-gradient(135deg, #FFF9C4, #FFF59D); border-color: #FDD835;">
                    <h4 style="color: #F57F17; margin-top: 0;">🚀 Moderate</h4>
                    <p style="font-size: 1.8rem; font-weight: 700; color: #F57F17; margin: 0.5rem 0;">
                        +{moderate['improvement']:.1f}
                    </p>
                    <p style="color: #666; margin: 0;">quintals/hectare</p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">Total gain: <strong>{gain_quintals:.0f} quintals</strong></p>
                    <p style="font-size: 0.85rem; color: #666;">{moderate['achievability']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with pot_col3:
                aggressive = improvement_potential['aggressive']
                gain_quintals = aggressive['improvement'] * st.session_state.farm_size
                st.markdown(f"""
                <div class="info-card" style="background: linear-gradient(135deg, #FFECB3, #FFE082); border-color: #FFB300;">
                    <h4 style="color: #E65100; margin-top: 0;">🏆 Aggressive</h4>
                    <p style="font-size: 1.8rem; font-weight: 700; color: #E65100; margin: 0.5rem 0;">
                        +{aggressive['improvement']:.1f}
                    </p>
                    <p style="color: #666; margin: 0;">quintals/hectare</p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">Total gain: <strong>{gain_quintals:.0f} quintals</strong></p>
                    <p style="font-size: 0.85rem; color: #666;">{aggressive['achievability']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Benchmark Comparison
            st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 1.5rem;"><i class="ri-line-chart-line"></i> Benchmark Comparison</h3>', unsafe_allow_html=True)
            
            # Create comparison bar chart
            comparison_data = pd.DataFrame([
                {'Category': 'Bottom 25%', 'Yield': benchmarks['bottom_25_percent']},
                {'Category': 'Average', 'Yield': benchmarks['average_yield']},
                {'Category': 'Your Yield', 'Yield': st.session_state.current_yield},
                {'Category': 'Top 25%', 'Yield': benchmarks['top_25_percent']},
                {'Category': 'Top 10%', 'Yield': benchmarks['top_10_percent']},
                {'Category': 'Maximum', 'Yield': benchmarks['max_yield_achieved']}
            ])
            
            fig2 = px.bar(
                comparison_data,
                x='Category',
                y='Yield',
                color='Category',
                color_discrete_map={
                    'Bottom 25%': '#FFCDD2',
                    'Average': '#B2DFDB',
                    'Your Yield': '#FF6B6B',
                    'Top 25%': '#81C784',
                    'Top 10%': '#4CAF50',
                    'Maximum': '#2E7D32'
                },
                text='Yield'
            )
            
            fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig2.update_layout(
                xaxis_title="",
                yaxis_title="Yield (quintals/hectare)",
                showlegend=False,
                height=350,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Data Context
            st.markdown(f"""
            <div class="info-card" style="margin-top: 1rem;">
                <p style="margin: 0;"><strong>📊 Analysis Based On:</strong></p>
                <p style="margin: 0.5rem 0 0 0; color: #666;">
                    {benchmarks['total_records']:,} records from {benchmarks['years_covered']} for 
                    <strong>{st.session_state.crop}</strong> in <strong>{st.session_state.state}</strong>
                    {f" during <strong>{selected_season}</strong> season" if selected_season else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown('<h3 style="color: var(--primary-green); margin-bottom: 1rem; margin-top: 1.5rem;"><i class="ri-lightbulb-line"></i> Personalized Recommendations</h3>', unsafe_allow_html=True)
            
            rec_col1, rec_col2 = st.columns(2)
            
            with rec_col1:
                st.markdown("""
                <div class="info-card">
                    <h4 style="color: var(--primary-green); margin-top: 0;">📈 Key Insights</h4>
                """, unsafe_allow_html=True)
                
                for rec in recommendations[:3]:
                    st.markdown(f"- {rec}")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with rec_col2:
                st.markdown("""
                <div class="info-card">
                    <h4 style="color: var(--primary-green); margin-top: 0;">💡 Action Items</h4>
                """, unsafe_allow_html=True)
                
                # Show high performer characteristics if available
                char = benchmarks['consistent_high_performers']['characteristics']
                if 'avg_fertilizer' in char:
                    st.markdown(f"- **Fertilizer:** {char['avg_fertilizer']:.0f} kg/ha (optimal range: {char['fertilizer_range']})")
                if 'optimal_pH' in char:
                    st.markdown(f"- **Soil pH:** {char['optimal_pH']:.1f}")
                    st.markdown(f"- **NPK:** N:{char['optimal_N']:.0f}, P:{char['optimal_P']:.0f}, K:{char['optimal_K']:.0f}")
                if 'optimal_temp' in char:
                    st.markdown(f"- **Temperature:** {char['optimal_temp']:.1f}°C")
                    st.markdown(f"- **Rainfall:** {char['optimal_rainfall']:.0f}mm")
                
                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; color: #666;">
            <i class="ri-file-chart-line" style="font-size: 4rem; color: var(--light-green);"></i>
            <h3 style="color: var(--text-dark); margin-top: 1rem;">No Analysis Yet</h3>
            <p>Fill in your farm details and click "Analyze Yield Gap" to see your performance analysis</p>
        </div>
        """, unsafe_allow_html=True)
