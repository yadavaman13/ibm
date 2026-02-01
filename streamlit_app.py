"""
Streamlit Farming Advisory System

A comprehensive web application for agricultural decision support with 3 advanced features:
1. Yield Gap Analysis & Benchmarking  
2. Multi-Scenario Outcome Predictor
3. Visual Explainable AI
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
from pathlib import Path
import cv2
from datetime import datetime, timedelta
import json
from PIL import Image, ImageDraw, ImageFont
import requests
import hashlib

# Import our custom modules (now in local directories)
from data_loader import DataLoader
from features.yield_gap_analyzer import YieldGapAnalyzer
from features.multi_scenario_predictor import MultiScenarioPredictor
from features.crop_disease_detector import CropDiseaseDetector
from language_translator import LanguageTranslator

# Initialize data and features
@st.cache_data
def load_agricultural_data():
    """Load and cache the agricultural datasets."""
    try:
        data_loader = DataLoader(".")  # Look in current directory (root)
        data_loader.load_datasets()
        return data_loader
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def initialize_session_state():
    """Initialize session state for disease tracking."""
    if 'disease_history' not in st.session_state:
        st.session_state.disease_history = []
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    if 'user_location' not in st.session_state:
        st.session_state.user_location = ""

@st.cache_resource  
def initialize_features(_data_loader):
    """Initialize the feature analyzers."""
    if _data_loader is None:
        return None, None, None, None
        
    try:
        gap_analyzer = YieldGapAnalyzer(_data_loader)
        scenario_predictor = MultiScenarioPredictor(_data_loader)
        disease_detector = CropDiseaseDetector(_data_loader)
        translator = LanguageTranslator()
        return gap_analyzer, scenario_predictor, disease_detector, translator
    except Exception as e:
        st.error(f"Error initializing features: {e}")
        return None, None, None, None

# Main app
def main():
    # Initialize session state first
    initialize_session_state()
    
    # Page config
    st.set_page_config(
        page_title="🌾 Smart Farming Assistant",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for farmer-friendly design
    st.markdown("""
    <style>
    .main {
        padding: 2rem 1rem;
    }
    .stSelectbox > div > div {
        font-size: 18px !important;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f1f8e9 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        text-align: center;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: 600;
    }
    .help-text {
        font-size: 16px;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #218838;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load data
    data_loader = load_agricultural_data()
    if data_loader is None:
        st.error("Failed to load agricultural data. Please ensure CSV files are in the parent directory.")
        st.stop()
        
    gap_analyzer, scenario_predictor, disease_detector, translator = initialize_features(data_loader)
    
    # Farmer-friendly sidebar
    with st.sidebar:
        st.markdown("## 🌍 अपनी भाषा चुनें / Choose Your Language")
        st.markdown('<p class="help-text">Select your preferred language for better understanding</p>', unsafe_allow_html=True)
        
        languages = translator.get_available_languages()
        selected_lang = st.selectbox(
            "Language / भाषा:",
            options=list(languages.keys()),
            format_func=lambda x: f"🗣️ {languages[x]}",
            index=0  # Default to English
        )
        
        st.markdown("---")
        st.markdown("## 📞 Need Help?")
        st.info("🤝 This system helps you make better farming decisions using data from thousands of farmers across India")
        
        st.markdown("### 🎯 What You Can Do:")
        st.markdown("""
        • **Compare** your crop yield with top farmers
        • **Predict** future crop performance  
        • **Detect** plant diseases from photos
        • **Plan** different farming strategies
        """)
        st.markdown("---")
    
    # Farmer-friendly header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        # 🌾 {translator.get_text('app_title', selected_lang)}
        <div class="big-font">{translator.get_text('app_subtitle', selected_lang)}</div>
        <div class="help-text">🚀 Smart farming decisions powered by data from 55 crops across 30 Indian states (1997-2020)</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Records", "19,689", "100% Complete Data")
        
    st.markdown("---")
    
    # Remove complex sidebar data summary and add simple navigation guide
    st.markdown("## 🧭 Choose What You Want To Do:")
    st.markdown('<p class="help-text">Click on any tab below to start using the farming tools</p>', unsafe_allow_html=True)
    
    # Simplified Navigation with farmer-friendly icons and descriptions  
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🏠 {translator.get_text('tab_home', selected_lang)}", 
        f"📊 {translator.get_text('tab_yield_gap', selected_lang)}", 
        f"🎯 {translator.get_text('tab_scenarios', selected_lang)}", 
        f"🧠 {translator.get_text('tab_prediction', selected_lang)}",
        f"🔬 {translator.get_text('tab_disease', selected_lang)}"
    ])
    
    with tab1:
        show_home_page(data_loader, translator, selected_lang)
    
    with tab2:
        show_yield_gap_analysis(data_loader, gap_analyzer, translator, selected_lang)
    
    with tab3:
        show_multi_scenario_predictor(data_loader, scenario_predictor, translator, selected_lang)
        
    with tab4:
        show_smart_prediction(data_loader, scenario_predictor, translator, selected_lang)
        
    with tab5:
        show_disease_detection(data_loader, disease_detector, translator, selected_lang)

def show_home_page(data_loader, translator, selected_lang):
    """Display the home page with simplified feature overview for farmers."""
    
    st.markdown(f"# 🚀 {translator.get_text('advanced_features', selected_lang)}")
    st.markdown('<p class="help-text">Choose the farming tool that best fits your needs. Each tool is designed to help you make better decisions.</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Larger, clearer feature cards for farmers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h2>📊 Compare Your Farm Performance</h2>
        <p style="font-size: 18px; margin: 1rem 0;">See how your crop yield compares with the best farmers in your region</p>
        <ul style="text-align: left; font-size: 16px;">
        <li>✅ Compare with top performers</li>
        <li>📈 Get improvement suggestions</li>  
        <li>🎯 Set realistic targets</li>
        <li>📋 Action plan for better yield</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h2>🧠 Predict Future Crops</h2>
        <p style="font-size: 18px; margin: 1rem 0;">Use AI to forecast your crop yield and plan ahead</p>
        <ul style="text-align: left; font-size: 16px;">
        <li>🤖 Smart AI predictions</li>
        <li>📊 Visual charts and graphs</li>
        <li>📈 Confidence in predictions</li>
        <li>📚 Learn from history</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h2>🎯 Test Different Strategies</h2>
        <p style="font-size: 18px; margin: 1rem 0;">Explore what happens if you change your farming approach</p>
        <ul style="text-align: left; font-size: 16px;">
        <li>🔍 Try different scenarios</li>
        <li>⚖️ Compare risks and benefits</li>
        <li>💰 Maximize your profits</li>
        <li>🤝 Get decision support</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h2>🔬 Detect Plant Diseases</h2>
        <p style="font-size: 18px; margin: 1rem 0;">Take a photo of your crop to identify diseases and get treatment advice</p>
        <ul style="text-align: left; font-size: 16px;">
        <li>📸 Photo-based diagnosis</li>
        <li>💊 Treatment recommendations</li>
        <li>⚠️ Assess disease severity</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simplified data showcase for farmers
    st.markdown("## 📈 Why Trust Our System?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Farm Records", "19,689", "Complete Data")
    with col2:
        st.metric("🌾 Crops Covered", "55", "Major Crops")  
    with col3:
        st.metric("🗺️ States Included", "30", "Across India")
    with col4:
        st.metric("📅 Years of Data", "24", "1997-2020")
    
    st.success("✅ Our recommendations are based on real data from thousands of successful farmers across India!")
    
    # Quick crop showcase in farmer's language
    st.markdown("### 🌾 Popular Crops Available")
    crops = data_loader.get_crop_list()
    
    # Show first 12 crops in a grid format
    crop_cols = st.columns(4)
    for i, crop in enumerate(crops[:12]):
        translated_crop = translator.translate_crop_name(crop, selected_lang)
        with crop_cols[i % 4]:
            st.markdown(f"**{translated_crop}**")
    
    if len(crops) > 12:
        st.markdown(f"*...and {len(crops) - 12} more crops available!*")

def show_yield_gap_analysis(data_loader, gap_analyzer, translator, selected_lang):
    """Display yield gap analysis interface with farmer-friendly guidance."""
    
    st.header(translator.get_text('tab_yield_gap', selected_lang))
    
    # Farmer-friendly explanation
    st.markdown("""
    <div class="feature-card">
    <h3>🎯 How This Helps You</h3>
    <p style="font-size: 18px;">This tool shows you how your crop yield compares with the best farmers in your area. You'll learn:</p>
    <ul style="font-size: 16px; text-align: left;">
    <li>📊 Where you stand compared to other farmers</li>
    <li>🚀 How much you can potentially improve</li>
    <li>💡 What the top farmers are achieving</li>
    <li>📈 Your improvement roadmap</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📝 Enter Your Farm Details")
    st.markdown('<p class="help-text">Fill in the information below to compare your yield with top performers</p>', unsafe_allow_html=True)
    
    # Simplified input form with better guidance
    with st.form("yield_gap_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            crop = st.selectbox(
                f"🌾 {translator.get_text('select_crop', selected_lang)}", 
                data_loader.get_crop_list(),
                help="Choose the main crop you want to analyze"
            )
            
            state = st.selectbox(
                f"🗺️ {translator.get_text('select_state', selected_lang)}", 
                data_loader.get_state_list(),
                help="Select your state for regional comparison"
            )
            
        with col2:
            user_yield = st.number_input(
                f"📊 {translator.get_text('your_yield', selected_lang)} (quintals per hectare)", 
                min_value=0.0, 
                max_value=200.0, 
                value=25.0,
                step=0.1,
                help="Enter your current average yield per hectare"
            )
            
            # Optional season filter
            seasons = data_loader.get_season_list()
            season = st.selectbox(
                f"🌦️ {translator.get_text('select_season', selected_lang)}", 
                ["All Seasons"] + seasons,
                help="Choose a specific season or keep 'All Seasons' for general comparison"
            )
            if season == "All Seasons":
                season = None
        
        st.markdown("---")
        submitted = st.form_submit_button(
            f"🔍 {translator.get_text('analyze_button', selected_lang)}", 
            type="primary",
            help="Click to see how you compare with top farmers"
        )
    
    if submitted and gap_analyzer:
        analyze_yield_gap(gap_analyzer, crop, state, season, user_yield, translator, selected_lang)

def analyze_yield_gap(gap_analyzer, crop, state, season, user_yield, translator, selected_lang):
    """Perform and display yield gap analysis with farmer-friendly explanations."""
    
    with st.spinner("📊 Analyzing your farm performance..."):
        gap_analysis = gap_analyzer.analyze_user_gap(user_yield, crop, state, season)
    
    if 'error' in gap_analysis:
        st.error(f"❌ {gap_analysis['error']}")
        if 'available_seasons' in gap_analysis:
            st.info(f"ℹ️ Available seasons: {', '.join(gap_analysis['available_seasons'])}")
        return
    
    # Farmer-friendly performance explanation
    st.markdown("## 🎯 Your Farm Performance Results")
    st.success(f"✅ Analysis complete for **{crop}** in **{state}**!")
    
    # Performance Dashboard with better explanations
    st.markdown("""
    <div class="metric-card">
    <h3>📊 How You Compare With Other Farmers</h3>
    <p>These numbers show where you stand compared to thousands of farmers in your region:</p>
    </div>
    """, unsafe_allow_html=True)
    
    benchmarks = gap_analysis['benchmarks']
    percentile_rank = gap_analysis['percentile_rank']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            translator.get_text('your_yield', selected_lang),
            f"{user_yield:.1f} q/ha", 
            f"{percentile_rank:.0f}{translator.get_text('percentile_suffix', selected_lang)}"
        )
        
    with col2:
        st.metric(
            translator.get_text('regional_average', selected_lang), 
            f"{benchmarks['average_yield']:.1f} q/ha",
            f"{user_yield - benchmarks['average_yield']:.1f} {translator.get_text('vs_you', selected_lang)}"
        )
        
    with col3:
        st.metric(
            translator.get_text('top_25_threshold', selected_lang),
            f"{benchmarks['top_25_percent']:.1f} q/ha",
            f"+{benchmarks['top_25_percent'] - user_yield:.1f} {translator.get_text('potential', selected_lang)}"
        )
        
    with col4:
        st.metric(
            translator.get_text('best_ever_recorded', selected_lang),
            f"{benchmarks['max_yield_achieved']:.1f} q/ha",
            f"+{benchmarks['max_yield_achieved'] - user_yield:.1f} {translator.get_text('maximum', selected_lang)}"
        )
    
    # Benchmarking Chart
    st.subheader(translator.get_text('benchmarking_comparison', selected_lang))
    
    benchmark_data = {
        'Category': [
            translator.get_text('bottom_25_percent', selected_lang), 
            translator.get_text('average', selected_lang), 
            translator.get_text('your_yield', selected_lang), 
            translator.get_text('top_25_percent', selected_lang), 
            translator.get_text('top_10_percent', selected_lang), 
            'Maximum'
        ],
        translator.get_text('yield_label', selected_lang): [
            benchmarks['bottom_25_percent'],
            benchmarks['average_yield'], 
            user_yield,
            benchmarks['top_25_percent'],
            benchmarks['top_10_percent'],
            benchmarks['max_yield_achieved']
        ],
        'Color': ['red', 'orange', 'blue', 'lightgreen', 'green', 'darkgreen']
    }
    
    fig = px.bar(
        x=benchmark_data['Yield'],
        y=benchmark_data['Category'],
        orientation='h',
        color=benchmark_data['Color'],
        color_discrete_map={color: color for color in benchmark_data['Color']},
        title="Yield Benchmarking Analysis"
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Improvement Potential
    st.subheader("🚀 Improvement Roadmap")
    
    improvement_potential = gap_analysis['improvement_potential']
    
    col1, col2, col3 = st.columns(3)
    
    scenarios = ['conservative', 'moderate', 'aggressive']
    titles = ['🎯 Short-term (3-6 months)', '🚀 Medium-term (6-12 months)', '🏆 Long-term (1+ years)']
    colors = ['info', 'warning', 'error']
    
    for i, (scenario, title, color) in enumerate(zip(scenarios, titles, colors)):
        with [col1, col2, col3][i]:
            if scenario in improvement_potential:
                potential = improvement_potential[scenario]
                if potential['improvement'] > 0:
                    st.metric(
                        title,
                        f"{potential['target_yield']:.1f} q/ha",
                        f"+{potential['improvement']:.1f} (+{potential['improvement_percent']:.1f}%)"
                    )
                    st.caption(potential['achievability'])
    
    # Recommendations
    st.subheader("💡 Personalized Recommendations")
    
    recommendations = gap_analysis['recommendations']
    for rec in recommendations:
        if rec.startswith('🏆'):
            st.success(rec)
        elif rec.startswith('👍'):
            st.info(rec)
        elif rec.startswith('📈'):
            st.warning(rec) 
        elif rec.startswith('🎯'):
            st.error(rec)
        else:
            st.write(rec)

def show_multi_scenario_predictor(data_loader, scenario_predictor, translator, selected_lang):
    """Display multi-scenario prediction interface."""
    
    st.header("🎯 Multi-Scenario Outcome Predictor")
    st.markdown("*Explore multiple 'what-if' scenarios for your farming decisions*")
    
    # Input form
    with st.form("scenario_form"):
        st.subheader("📝 Base Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop = st.selectbox("🌱 Crop", data_loader.get_crop_list())
            state = st.selectbox("📍 State", data_loader.get_state_list())
            
        with col2:
            season = st.selectbox("🗓️ Season", data_loader.get_season_list())
            area = st.number_input("📏 Area (hectares)", min_value=0.1, value=1.0, step=0.1)
            
        with col3:
            fertilizer = st.number_input("🧪 Fertilizer (kg/ha)", min_value=0, value=25000, step=1000)
            pesticide = st.number_input("🦗 Pesticide (kg/ha)", min_value=0, value=500, step=50)
        
        st.subheader("🌤️ Environmental Conditions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_temp = st.number_input("🌡️ Avg Temperature (°C)", min_value=10.0, max_value=45.0, value=25.0)
            rainfall = st.number_input("🌧️ Total Rainfall (mm)", min_value=100, max_value=3000, value=1000)
            
        with col2:
            humidity = st.number_input("💧 Avg Humidity (%)", min_value=30, max_value=100, value=70)
            pH = st.number_input("🔬 Soil pH", min_value=4.0, max_value=9.0, value=6.5, step=0.1)
            
        with col3:
            N = st.number_input("🧪 Nitrogen (N)", min_value=20, max_value=200, value=75)
            P = st.number_input("🧪 Phosphorus (P)", min_value=10, max_value=80, value=35)
            K = st.number_input("🧪 Potassium (K)", min_value=10, max_value=60, value=30)
        
        submitted = st.form_submit_button("🔮 Generate Scenarios", type="primary")
    
    if submitted and scenario_predictor:
        predict_multiple_scenarios(
            scenario_predictor, crop, state, season, area, fertilizer, 
            pesticide, avg_temp, rainfall, humidity, pH, N, P, K
        )

def predict_multiple_scenarios(scenario_predictor, crop, state, season, area, fertilizer, pesticide, avg_temp, rainfall, humidity, pH, N, P, K):
    """Generate and display multiple scenario predictions."""
    
    # Prepare base parameters
    base_params = {
        'crop': crop, 'state': state, 'season': season, 'area': area,
        'fertilizer': fertilizer, 'pesticide': pesticide, 'avg_temp_c': avg_temp,
        'total_rainfall_mm': rainfall, 'avg_humidity_percent': humidity,
        'pH': pH, 'N': N, 'P': P, 'K': K
    }
    
    with st.spinner("Generating multiple scenarios..."):
        # Create scenarios
        scenarios = scenario_predictor.create_scenarios(base_params)
        
        # Predict outcomes
        scenario_results = scenario_predictor.predict_scenarios(scenarios)
        
        # Generate comparison
        comparison = scenario_predictor.compare_scenarios(scenario_results)
    
    if not scenario_results:
        st.error("Could not generate scenario predictions. Please check your inputs.")
        return
    
    # Scenario Comparison Table
    st.subheader("📊 Scenario Comparison")
    
    scenario_df = pd.DataFrame([
        {
            'Scenario': result['scenario_name'],
            'Predicted Yield': f"{result['predicted_yield']:.1f} q/ha",
            'Risk Level': result['risk_level'].title(),
            'Profit': f"₹{result['estimated_profit']['profit']:,.0f}",
            'Confidence Range': result['yield_range']
        }
        for result in scenario_results
    ])
    
    st.dataframe(scenario_df, use_container_width=True)
    
    # Scenario Comparison Chart
    st.subheader("📈 Yield vs Profit Analysis")
    
    yields = [r['predicted_yield'] for r in scenario_results]
    profits = [r['estimated_profit']['profit'] for r in scenario_results]
    names = [r['scenario_name'] for r in scenario_results]
    colors = [{'low': 'green', 'medium': 'orange', 'high': 'red'}[r['risk_level']] for r in scenario_results]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add yield bars
    fig.add_trace(
        go.Bar(x=names, y=yields, name="Predicted Yield", marker_color=colors, opacity=0.7),
        secondary_y=False
    )
    
    # Add profit line  
    fig.add_trace(
        go.Scatter(x=names, y=profits, mode='lines+markers', name="Profit", line=dict(color='blue', width=3)),
        secondary_y=True
    )
    
    fig.update_yaxes(title_text="Yield (quintal/ha)", secondary_y=False)
    fig.update_yaxes(title_text="Profit (₹)", secondary_y=True)
    fig.update_layout(title="Scenario Comparison: Yield vs Profit", height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk vs Return Scatter
    st.subheader("⚖️ Risk vs Return Analysis")
    
    risk_mapping = {'low': 1, 'medium': 2, 'high': 3}
    risk_scores = [risk_mapping[r['risk_level']] for r in scenario_results]
    
    # Ensure positive size values for scatter plot
    min_profit = min(profits)
    size_values = [p - min_profit + 1000 for p in profits]  # Add offset to make all positive
    
    fig = px.scatter(
        x=risk_scores, y=yields, text=names, size=size_values,
        labels={'x': 'Risk Level (1=Low, 2=Medium, 3=High)', 'y': 'Expected Yield (quintal/ha)'},
        title="Risk vs Return Analysis"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("🎯 Smart Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_yield = comparison['best_for_yield']
        st.success(f"""
        **🏆 Highest Yield**  
        {best_yield['scenario']}  
        **{best_yield['yield']:.1f} quintal/ha**  
        +{best_yield['improvement_over_baseline']:.1f} vs baseline
        """)
    
    with col2:
        best_profit = comparison['best_for_profit'] 
        st.info(f"""
        **💰 Highest Profit**  
        {best_profit['scenario']}  
        **₹{best_profit['profit']:,.0f}**  
        +₹{best_profit['improvement_over_baseline']:,.0f} vs baseline
        """)
    
    with col3:
        lowest_risk = comparison['lowest_risk']
        st.warning(f"""
        **🛡️ Safest Option**  
        {lowest_risk['scenario']}  
        **{lowest_risk['yield']:.1f} quintal/ha**  
        Risk: {lowest_risk['risk_level'].title()}
        """)
    
    # Decision Tree
    st.subheader("🌳 Decision Guide")
    
    recommendations = comparison['recommendations']
    for rec in recommendations:
        st.write(f"• {rec}")

def show_smart_prediction(data_loader, scenario_predictor, translator, selected_lang):
    """Display smart yield prediction with explanations."""
    
    st.header("🧠 Smart Yield Prediction with AI Explanations")
    st.markdown("*Get detailed insights into your yield prediction*")
    
    # Simple input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            crop = st.selectbox("🌱 Crop", data_loader.get_crop_list())
            state = st.selectbox("📍 State", data_loader.get_state_list())
            season = st.selectbox("🗓️ Season", data_loader.get_season_list())
            
        with col2:
            fertilizer = st.number_input("🧪 Fertilizer (kg/ha)", value=25000)
            pH = st.number_input("🔬 Soil pH", min_value=4.0, max_value=9.0, value=6.5)
            rainfall = st.number_input("🌧️ Rainfall (mm)", value=1000)
        
        submitted = st.form_submit_button("🔮 Predict Yield", type="primary")
    
    if submitted and scenario_predictor:
        make_smart_prediction(scenario_predictor, crop, state, season, fertilizer, pH, rainfall, data_loader)

def make_smart_prediction(scenario_predictor, crop, state, season, fertilizer, pH, rainfall, data_loader):
    """Make prediction with detailed explanations."""
    
    # Prepare input
    user_inputs = {
        'crop': crop, 'state': state, 'season': season,
        'area': 1, 'fertilizer': fertilizer, 'pesticide': 500,
        'avg_temp_c': 25, 'total_rainfall_mm': rainfall, 'avg_humidity_percent': 70,
        'pH': pH, 'N': 75, 'P': 35, 'K': 30,
        'scenario_name': 'Your Prediction', 'scenario_type': 'user_input'
    }
    
    with st.spinner("Making AI prediction..."):
        results = scenario_predictor.predict_scenarios([user_inputs])
    
    if not results:
        st.error("Could not generate prediction.")
        return
    
    prediction = results[0]
    
    # Main prediction display
    st.subheader("🎯 Your Prediction Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Predicted Yield",
            f"{prediction['predicted_yield']:.1f} quintal/ha",
            f"Range: {prediction['yield_range']}"
        )
    
    with col2:
        risk_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        st.metric(
            "Risk Level",
            f"{risk_color[prediction['risk_level']]} {prediction['risk_level'].title()}",
            "Prediction uncertainty"
        )
    
    with col3:
        st.metric(
            "Estimated Profit",
            f"₹{prediction['estimated_profit']['profit']:,.0f}",
            f"₹{prediction['estimated_profit']['profit_per_hectare']:,.0f}/ha"
        )
    
    # Historical Context
    st.subheader("📈 Historical Context")
    
    historical_data = data_loader.filter_data(crop=crop, state=state, season=season)
    
    if not historical_data.empty:
        historical_avg = historical_data['yield'].mean()
        historical_max = historical_data['yield'].max()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Regional Historical Performance**  
            Average: {historical_avg:.1f} quintal/ha  
            Best ever: {historical_max:.1f} quintal/ha  
            Records: {len(historical_data)} data points
            """)
        
        with col2:
            if prediction['predicted_yield'] > historical_avg:
                st.success(f"✅ Your prediction is {prediction['predicted_yield'] - historical_avg:.1f} quintal/ha **above** regional average!")
            else:
                st.warning(f"⚠️ Your prediction is {historical_avg - prediction['predicted_yield']:.1f} quintal/ha **below** regional average")
    
    # Yield Distribution Chart
    if not historical_data.empty:
        st.subheader("📊 How You Compare")
        
        fig = px.histogram(
            historical_data, x='yield', 
            title=f'Yield Distribution: {crop} in {state}',
            labels={'yield': 'Yield (quintal/ha)', 'count': 'Number of Records'}
        )
        
        # Add your prediction line
        fig.add_vline(
            x=prediction['predicted_yield'],
            line_dash="dash", line_color="red",
            annotation_text=f"Your Prediction: {prediction['predicted_yield']:.1f}",
            annotation_position="top"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Reasoning
    st.subheader("🧠 AI Reasoning")
    
    st.write("**How we made this prediction:**")
    st.write("• Analyzed 24 years of agricultural data (1997-2020)")
    st.write(f"• Used 19,689+ historical records from {state}")
    st.write(f"• AI model trained on similar {crop} farms")
    st.write("• Considered soil conditions, weather patterns, and farming practices")
    st.write("• Cross-validated for accuracy and reliability")
    
    # Key Factors
    with st.expander("🔍 Key Factors Analysis"):
        
        st.write("**Your Input Analysis:**")
        
        if fertilizer < 20000:
            st.warning(f"💡 **Fertilizer**: You're using {fertilizer:,} kg/ha. Consider increasing for better yield")
        elif fertilizer > 40000:
            st.error(f"⚠️ **Fertilizer**: You're using {fertilizer:,} kg/ha. This might be excessive")
        else:
            st.success(f"✅ **Fertilizer**: Your {fertilizer:,} kg/ha is in reasonable range")
        
        if pH < 6.0:
            st.warning(f"🔬 **Soil pH**: {pH:.1f} is acidic. Consider liming")
        elif pH > 8.0:
            st.warning(f"🔬 **Soil pH**: {pH:.1f} is alkaline. Consider organic matter") 
        else:
            st.success(f"✅ **Soil pH**: {pH:.1f} is in good range")
        
        if rainfall < 500:
            st.warning(f"🌧️ **Rainfall**: {rainfall}mm might be insufficient for {crop}")
        elif rainfall > 2000:
            st.warning(f"🌧️ **Rainfall**: {rainfall}mm might be excessive for {crop}")
        else:
            st.success(f"✅ **Rainfall**: {rainfall}mm is suitable for {crop}")

def show_disease_detection(data_loader, disease_detector, translator, selected_lang):
    """Enhanced AI-powered crop disease detection interface with multiple features."""
    
    st.header("Crop Disease Detection")
    st.markdown("*Upload or capture photos for AI-powered disease analysis and treatment recommendations*")
    
    # Disease progression tracking display
    if hasattr(st.session_state, 'disease_history') and st.session_state.disease_history:
        with st.expander(f"Analysis History ({len(st.session_state.disease_history)} previous analyses)", expanded=False):
            show_disease_progression_timeline()
    
    # Image capture/upload section with tabs
    st.subheader("Image Upload Options")
    
    tab1, tab2 = st.tabs(["Camera Capture", "File Upload"])
    
    with tab1:
        st.markdown("**Real-time Camera Capture**")
        camera_photo = st.camera_input("Take a photo of your crop", help="Position camera to focus on affected plant parts")
        if camera_photo:
            st.success("Photo captured successfully")
            # Show small preview
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(camera_photo, caption="Camera Preview", width=200)
    
    with tab2:
        st.markdown("**Upload Crop Photos**")
        uploaded_files = st.file_uploader(
            "Choose one or more images of your crop",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload 1 image for single analysis or multiple photos for comprehensive analysis"
        )
        if uploaded_files:
            if len(uploaded_files) == 1:
                st.success("1 photo uploaded - Single image analysis ready")
                # Show single preview
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(uploaded_files[0], caption="Upload Preview", width=200)
            else:
                st.success(f"{len(uploaded_files)} photos uploaded - Multiple image analysis ready")
                # Show small previews in a grid
                st.markdown("**Preview of uploaded images:**")
                if len(uploaded_files) <= 3:
                    cols = st.columns(len(uploaded_files))
                    for i, file in enumerate(uploaded_files):
                        with cols[i]:
                            st.image(file, caption=f"Photo {i+1}", width=150)
                else:
                    # Show in rows of 3 for more than 3 images
                    for i in range(0, len(uploaded_files), 3):
                        batch = uploaded_files[i:i+3]
                        cols = st.columns(len(batch))
                        for j, file in enumerate(batch):
                            with cols[j]:
                                st.image(file, caption=f"Photo {i+j+1}", width=120)
    
    # Analysis Parameters
    st.subheader("Analysis Settings")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        crop_type = st.selectbox("Select Crop Type", 
            ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato', 'Corn', 'Other'])
        
        location = st.text_input("Location (optional)", 
            value=getattr(st.session_state, 'user_location', ''),
            placeholder="e.g., Punjab, Maharashtra",
            help="Used for local treatment cost estimation")
        if location:
            st.session_state.user_location = location
    
    with col2:
        st.info("""
        **Enhanced Analysis Features:**
        • Real-time camera capture
        • Smart symptom highlighting  
        • Local treatment cost estimation
        • Disease progression tracking
        • Automatic single/multiple analysis
        """)
    
    # Determine which photos to analyze
    photos_to_analyze = []
    if camera_photo:
        photos_to_analyze.append(("Camera", camera_photo))
    if uploaded_files:
        for i, file in enumerate(uploaded_files):
            photos_to_analyze.append((f"Upload-{i+1}", file))
    
    if photos_to_analyze:
        # Ready for analysis section
        st.subheader(f"Analysis Ready ({len(photos_to_analyze)} photos)")
        
        # Enhanced analysis button
        analysis_type = "Multiple Photo Analysis" if len(photos_to_analyze) > 1 else "Single Photo Analysis"
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button(f"Run {analysis_type}", type="primary", help="Start AI analysis with symptom highlighting and cost estimation"):
                analyze_enhanced_crop_disease(photos_to_analyze, crop_type, location, disease_detector)
        with col2:
            st.info(f"{len(photos_to_analyze)} image(s) ready for analysis")
    
    else:
        # Demo section when no image is uploaded
        st.subheader("Demo Analysis")
        
        demo_scenarios = {
            "Rice Leaf Spot (Moderate)": {"crop": "Rice", "disease": "leaf_spot", "severity": "moderate"},
            "Wheat Rust Disease (Mild)": {"crop": "Wheat", "disease": "rust_disease", "severity": "mild"},
            "Cotton Bacterial Blight (Severe)": {"crop": "Cotton", "disease": "bacterial_blight", "severity": "severe"},
            "Healthy Plant (No Disease)": {"crop": "Tomato", "disease": "healthy", "severity": "none"},
        }
        
        selected_demo = st.selectbox("Select a demo scenario:", list(demo_scenarios.keys()))
        
        if st.button("Run Demo Analysis"):
            demo_data = demo_scenarios[selected_demo]
            run_enhanced_demo_analysis(demo_data, disease_detector, location)
    
    # Educational content
    show_disease_education(disease_detector)

def analyze_enhanced_crop_disease(photos_data, crop_type, location, disease_detector):
    """Enhanced analysis with multiple photos, symptom highlighting, cost calculation, and image validation."""
    
    with st.spinner(f"🔬 Analyzing {len(photos_data)} photo(s) for crop content and diseases... This may take a few moments."):
        
        # Analyze all photos
        all_analyses = []
        invalid_images = []
        
        for source, photo in photos_data:
            image_data = photo.read()
            analysis = disease_detector.analyze_image(image_data, crop_type, location)
            analysis['source'] = source
            
            # Check if image is valid crop image
            if not analysis.get('is_valid_crop_image', True):
                invalid_images.append((source, analysis))
            else:
                all_analyses.append(analysis)
        
        # Handle case where no valid crop images were found
        if not all_analyses:
            st.error("**No Valid Crop Images Detected**")
            
            st.markdown("### Image Validation Results")
            
            for source, analysis in invalid_images:
                with st.expander(f"Invalid Image: {source}", expanded=True):
                    st.warning(f"**{analysis.get('validation_message', 'Image validation failed')}**")
                    
                    if 'image_validation' in analysis and analysis['image_validation']:
                        validation = analysis['image_validation']
                        
                        # Show what was detected
                        if 'detected_content' in validation:
                            st.info(f"**Detected Content:** {validation['detected_content']}")
                        
                        # Show validation details
                        st.markdown("**Analysis Details:**")
                        for detail in validation.get('details', []):
                            st.markdown(f"• {detail}")
                        
                        # Show suggestions
                        if 'suggestions' in validation:
                            st.markdown("**Suggestions for Better Results:**")
                            for suggestion in validation['suggestions']:
                                st.markdown(f"• {suggestion}")
            
            # Provide general guidance
            st.markdown("""
            ---
            ### How to Take Good Crop Photos
            
            **Do:**
            • Take photos of actual crops, plants, or leaves
            • Use natural daylight for best results
            • Get close to show plant details clearly
            • Include areas with visible symptoms
            • Take multiple angles of the same plant
            
            **Don't:**
            • Upload icons, graphics, or logos
            • Use very dark or blurry images
            • Photograph non-plant objects
            • Use heavily filtered or edited images
            """)
            return
        
        # Show warnings for any invalid images
        if invalid_images:
            st.warning(f"⚠️ **{len(invalid_images)} out of {len(photos_data)} images were not valid crop images and were excluded from analysis.**")
            
            with st.expander(f"View Invalid Images ({len(invalid_images)})", expanded=False):
                for source, analysis in invalid_images:
                    st.error(f"**{source}:** {analysis.get('validation_message', 'Invalid crop image')}")
        
        # Aggregate results for valid images
        if len(all_analyses) > 1:
            aggregated_analysis = disease_detector.aggregate_multi_photo_analysis(all_analyses)
            st.success(f"✅ **Enhanced Analysis Complete!** Analyzed {len(all_analyses)} valid crop images.")
        else:
            aggregated_analysis = all_analyses[0]
            st.success("✅ **Analysis Complete!** Valid crop image analyzed successfully.")
        
        # Store in disease history
        if not hasattr(st.session_state, 'disease_history'):
            st.session_state.disease_history = []
        if not hasattr(st.session_state, 'analysis_count'):
            st.session_state.analysis_count = 0
            
        history_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'crop_type': crop_type,
            'location': location,
            'analysis': aggregated_analysis,
            'photo_count': len(all_analyses),
            'invalid_photos': len(invalid_images)
        }
        st.session_state.disease_history.append(history_entry)
        st.session_state.analysis_count += 1
    
    # Display enhanced results for valid crop images
    show_image_validation_summary(aggregated_analysis)
    
    # Analysis Summary with enhanced metrics
    st.subheader("Analysis Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Confidence Score", f"{aggregated_analysis['confidence_score']:.0%}")
    
    with col2:
        st.metric("Valid Photos", len(all_analyses))
    
    with col3:
        st.metric("Image Quality", aggregated_analysis['image_quality']['score'])
    
    with col4:
        st.metric("Urgency Level", aggregated_analysis['urgency_level'])
    
    with col5:
        diseases_count = len([d for d in aggregated_analysis['diseases_detected'] if d['disease_id'] != 'healthy'])
        st.metric("Issues Found", diseases_count)
    
    with col3:
        st.metric("Image Quality", aggregated_analysis['image_quality']['score'])
    
    with col4:
        st.metric("Urgency Level", aggregated_analysis['urgency_level'])
    
    with col5:
        diseases_count = len([d for d in aggregated_analysis['diseases_detected'] if d['disease_id'] != 'healthy'])
        st.metric("Issues Found", diseases_count)
    
    # Smart symptom highlighting (simulated)
    if len(photos_data) == 1:
        show_symptom_highlighting(photos_data[0][1], aggregated_analysis)
    
    # Disease detection results with enhanced features
    show_enhanced_disease_results(aggregated_analysis, crop_type, location, disease_detector)
    
    # Treatment cost calculator
    if location:
        show_treatment_cost_calculator(aggregated_analysis, location, crop_type)

def show_image_validation_summary(analysis):
    """Display image validation summary for valid crop images."""
    
    if 'image_validation' in analysis:
        validation = analysis['image_validation']
        
        with st.expander("Image Validation Details", expanded=False):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.success(f"**Crop Image Validated**")
                st.metric("Validation Confidence", f"{validation.get('confidence', 0.9):.0%}")
                
                if 'details' in validation:
                    st.markdown("**Validation Details:**")
                    for detail in validation['details'][:3]:  # Show top 3 details
                        st.markdown(f"• {detail}")
            
            with col2:
                st.info("""
                **Validation Criteria:**
                • Plant/crop content detection
                • Natural color patterns
                • Organic shape analysis  
                • Texture assessment
                • Edge pattern evaluation
                """)

def show_symptom_highlighting(image, analysis):
    """Display image with highlighted symptoms."""
    st.subheader("🎯 Smart Symptom Highlighting")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    
    with col2:
        # Simulate symptom highlighting
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        
        # Simulate highlighting affected areas (random circles for demo)
        width, height = img.size
        for disease in analysis['diseases_detected']:
            if disease['disease_id'] != 'healthy':
                # Simulate highlighting with colored circles
                for _ in range(3):  # 3 affected areas
                    x = np.random.randint(50, width-50)
                    y = np.random.randint(50, height-50)
                    radius = np.random.randint(20, 40)
                    
                    # Different colors for different severity levels
                    if disease['severity'] == 'severe':
                        color = 'red'
                    elif disease['severity'] == 'moderate':
                        color = 'orange'
                    else:
                        color = 'yellow'
                    
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               outline=color, width=3)
        
        st.image(img, caption="🎯 Highlighted Symptoms", use_container_width=True)
        
        st.info("""
        **🎯 Highlighting Legend:**
        - 🔴 **Red**: Severe symptoms
        - 🟠 **Orange**: Moderate symptoms  
        - 🟡 **Yellow**: Mild symptoms
        """)

def show_treatment_cost_calculator(analysis, location, crop_type):
    """Display treatment cost calculation with local pricing."""
    st.subheader("💰 Treatment Cost Calculator")
    
    # Simulate local pricing based on location
    location_multipliers = {
        'punjab': 0.9, 'haryana': 0.95, 'maharashtra': 1.1, 'karnataka': 1.05,
        'tamil nadu': 1.08, 'gujarat': 1.02, 'rajasthan': 0.93, 'uttar pradesh': 0.88
    }
    
    location_lower = location.lower()
    multiplier = 1.0
    for state in location_multipliers:
        if state in location_lower:
            multiplier = location_multipliers[state]
            break
    
    total_cost = 0
    cost_breakdown = []
    
    for disease in analysis['diseases_detected']:
        if disease['disease_id'] != 'healthy':
            base_cost = disease.get('treatment_cost', 1000)
            local_cost = base_cost * multiplier
            total_cost += local_cost
            
            cost_breakdown.append({
                'Disease': disease['name'],
                'Severity': disease['severity'].title(),
                'Base Cost (₹)': f"{base_cost:,.0f}",
                'Local Cost (₹)': f"{local_cost:,.0f}",
                'Urgency': '🔴 High' if disease['severity'] == 'severe' else 
                          '🟠 Medium' if disease['severity'] == 'moderate' else '🟡 Low'
            })
    
    if cost_breakdown:
        # Cost summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Treatment Cost", f"₹{total_cost:,.0f}")
        
        with col2:
            savings = total_cost * 0.15 if len(analysis['diseases_detected']) > 1 else 0
            st.metric("Early Detection Savings", f"₹{savings:,.0f}")
        
        with col3:
            net_cost = total_cost - savings
            st.metric("Final Cost", f"₹{net_cost:,.0f}")
        
        # Detailed breakdown
        st.subheader("📊 Cost Breakdown")
        df_costs = pd.DataFrame(cost_breakdown)
        st.dataframe(df_costs, use_container_width=True)
        
        # Regional pricing info
        st.info(f"""
        **📍 Regional Pricing for {location}:**
        - Price multiplier: {multiplier:.1%}
        - Includes: Pesticides, labor, equipment rental
        - Excludes: Transportation, expert consultation fees
        """)
        
        # Treatment scheduling
        st.subheader("📅 Recommended Treatment Schedule")
        show_treatment_schedule(analysis, crop_type)

def show_treatment_schedule(analysis, crop_type):
    """Display recommended treatment schedule."""
    
    # Create treatment timeline
    today = datetime.now()
    schedule = []
    
    for disease in analysis['diseases_detected']:
        if disease['disease_id'] != 'healthy':
            if disease['severity'] == 'severe':
                # Immediate treatment needed
                schedule.append({
                    'Date': today.strftime('%Y-%m-%d'),
                    'Day': 'Day 1 (Today)',
                    'Treatment': f'Emergency treatment for {disease["name"]}',
                    'Action': 'Apply systemic fungicide + Remove affected parts',
                    'Priority': '🔴 Critical'
                })
                schedule.append({
                    'Date': (today + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'Day': 'Day 4',
                    'Treatment': 'Follow-up inspection',
                    'Action': 'Assess treatment effectiveness',
                    'Priority': '🟠 Important'
                })
            else:
                # Regular treatment
                schedule.append({
                    'Date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
                    'Day': 'Day 2',
                    'Treatment': f'Treatment for {disease["name"]}',
                    'Action': 'Apply preventive measures',
                    'Priority': '🟡 Moderate'
                })
    
    if schedule:
        df_schedule = pd.DataFrame(schedule)
        st.dataframe(df_schedule, use_container_width=True)
        
        if st.button("📱 Set Treatment Reminders"):
            st.success("📅 Treatment reminders would be set in a full implementation!")

def show_disease_progression_timeline():
    """Display disease progression timeline from session state."""
    
    if not hasattr(st.session_state, 'disease_history') or not st.session_state.disease_history:
        st.info("No previous analyses found.")
        return
    
    # Create timeline visualization
    timeline_data = []
    for i, entry in enumerate(st.session_state.disease_history):
        diseases = entry['analysis']['diseases_detected']
        disease_names = [d['name'] for d in diseases if d['disease_id'] != 'healthy']
        
        timeline_data.append({
            'Analysis #': i + 1,
            'Date': entry['timestamp'][:10],
            'Time': entry['timestamp'][11:],
            'Crop': entry['crop_type'],
            'Location': entry['location'],
            'Diseases Found': len(disease_names),
            'Disease Names': ', '.join(disease_names) if disease_names else 'Healthy'
        })
    
    if timeline_data:
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True)
        
        # Progression chart
        if len(timeline_data) > 1:
            fig = px.line(df_timeline, x='Analysis #', y='Diseases Found', 
                         title='Disease Detection Over Time',
                         markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def show_enhanced_disease_results(analysis, crop_type, location, disease_detector):
    """Display enhanced disease results with detailed information."""
    
    st.subheader("Disease Detection Results")
    
    diseases = analysis['diseases_detected']
    
    if diseases[0]['disease_id'] == 'healthy':
        st.success("**Excellent News! No diseases detected in your crop.**")
        
        # Provide preventive recommendations even for healthy crops
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.info("""
            **Keep Your Crop Healthy:**
            • Continue regular monitoring
            • Maintain proper irrigation
            • Ensure good air circulation
            • Apply preventive treatments
            """)
        
        with col2:
            st.success("""
            **Next Steps:**
            • Check again in 7 days
            • Monitor weather conditions
            • Track growth patterns
            • Document with photos
            """)
    else:
        # Display each disease with enhanced information
        for i, disease in enumerate(diseases):
            severity_indicator = "🔴" if disease['severity'] == 'severe' else "🟠" if disease['severity'] == 'moderate' else "🟡"
            
            with st.expander(f"{disease['name']} - Severity: {disease['severity'].title()}", expanded=True):
                
                # Enhanced disease information in columns
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # Get enhanced treatment plan
                    treatment_plan = disease_detector.get_enhanced_treatment_plan(
                        disease['disease_id'], disease['severity'], crop_type, location
                    )
                    
                    st.markdown(f"**Confidence:** {disease['confidence']:.0%}")
                    st.markdown(f"**Severity:** {disease['severity'].title()}")
                    st.markdown(f"**Affected Crop:** {crop_type}")
                    
                    # Immediate actions
                    st.markdown("**Immediate Actions (Next 24 hours):**")
                    for action in treatment_plan.get('immediate_actions', []):
                        st.markdown(f"• {action}")
                
                with col2:
                    # Risk assessment
                    st.markdown("**Risk Assessment:**")
                    risk_level = disease.get('risk_level', 'Medium')
                    st.markdown(f"**Spread Risk:** {risk_level}")
                    st.markdown(f"**Yield Impact:** {disease.get('yield_impact', '10-15%')}")
                    
                    # Weather factor
                    st.markdown("**Weather Factor:**")
                    st.markdown("Moderate risk conditions")
                
                with col3:
                    # Quick stats
                    st.markdown("**Quick Stats:**")
                    st.markdown(f"**Prevalence:** {disease.get('prevalence', '15%')} in region")
                    st.markdown(f"**Seasonal Risk:** {disease.get('seasonal_risk', 'High')} (current season)")
                    
                    # Action urgency
                    urgency = disease['severity']
                    if urgency == 'severe':
                        st.error("Act immediately!")
                    elif urgency == 'moderate':
                        st.warning("Act within 2-3 days")
                    else:
                        st.info("Monitor closely")

def run_enhanced_demo_analysis(demo_data, disease_detector, location):
    """Run enhanced demo analysis with simulated comprehensive results."""
    
    with st.spinner("🔬 Running enhanced demo analysis..."):
        # Simulate enhanced analysis
        import time
        time.sleep(2)
        
        # Create mock analysis data
        mock_analysis = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'crop_type': demo_data['crop'],
            'location': location or 'Demo Location',
            'confidence_score': 0.87,
            'image_quality': {'score': 'Excellent', 'rating': 9.2},
            'urgency_level': demo_data['severity'].title(),
            'diseases_detected': [
                {
                    'disease_id': demo_data['disease'],
                    'name': f"{demo_data['crop']} {demo_data['disease'].replace('_', ' ').title()}",
                    'severity': demo_data['severity'],
                    'confidence': 0.87,
                    'treatment_cost': 1500 if demo_data['severity'] == 'severe' else 800,
                    'risk_level': 'High' if demo_data['severity'] == 'severe' else 'Medium',
                    'yield_impact': '20-30%' if demo_data['severity'] == 'severe' else '10-15%',
                    'prevalence': '18%',
                    'seasonal_risk': 'High'
                }
            ] if demo_data['disease'] != 'healthy' else [
                {
                    'disease_id': 'healthy',
                    'name': 'Healthy Plant',
                    'severity': 'none',
                    'confidence': 0.92
                }
            ]
        }
        
        # Store in history
        if not hasattr(st.session_state, 'disease_history'):
            st.session_state.disease_history = []
            
        history_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'crop_type': demo_data['crop'],
            'location': location or 'Demo Location',
            'analysis': mock_analysis,
            'photo_count': 1
        }
        st.session_state.disease_history.append(history_entry)
    
    st.success("✅ Enhanced Demo Analysis Complete!")
    
    # Display results using enhanced functions
    show_enhanced_disease_results(mock_analysis, demo_data['crop'], location, disease_detector)
    
    if location and mock_analysis['diseases_detected'][0]['disease_id'] != 'healthy':
        show_treatment_cost_calculator(mock_analysis, location, demo_data['crop'])

def analyze_crop_disease(uploaded_file, crop_type, location, disease_detector):
    """Analyze uploaded image for crop diseases."""
    
    with st.spinner("🔬 Analyzing image with AI... This may take a few moments."):
        
        # Convert uploaded file to image data
        image_data = uploaded_file.read()
        
        # Run AI analysis
        analysis_report = disease_detector.analyze_image(image_data, crop_type, location)
    
    # Display results
    st.success("✅ Analysis Complete!")
    
    # Analysis Summary
    st.subheader("📋 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Confidence Score", f"{analysis_report['confidence_score']:.0%}")
    
    with col2:
        st.metric("Image Quality", analysis_report['image_quality']['score'])
    
    with col3:
        st.metric("Urgency Level", analysis_report['urgency_level'])
    
    with col4:
        diseases_count = len([d for d in analysis_report['diseases_detected'] if d['disease_id'] != 'healthy'])
        st.metric("Issues Found", diseases_count)
    
    # Disease Detection Results
    st.subheader("🦠 Disease Detection Results")
    
    diseases = analysis_report['diseases_detected']
    
    if diseases[0]['disease_id'] == 'healthy':
        st.success("🎉 **Great News! No diseases detected in your crop.**")
        st.info("Continue with regular monitoring and preventive care.")
    else:
        for i, disease in enumerate(diseases):
            with st.expander(f"🔍 {disease['name']} - Severity: {disease['severity'].title()}", expanded=True):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Get detailed treatment plan
                    treatment_plan = disease_detector.get_treatment_plan(
                        disease['disease_id'], disease['severity'], crop_type
                    )
                    
                    st.write(f"**Confidence:** {disease['confidence']:.0%}")
                    st.write(f"**Severity:** {disease['severity'].title()}")
                    
                    # Treatment recommendations
                    st.write("**🏥 Immediate Actions:**")
                    for action in treatment_plan['immediate_actions']:
                        st.write(f"• {action}")
                    
                    st.write("**💊 Complete Treatment Plan:**")
                    for treatment in treatment_plan['treatments']:
                        st.write(f"• {treatment}")
                
                with col2:
                    st.info(f"""
                    **📊 Treatment Details**
                    
                    **Timeline:** {treatment_plan['timeline']}
                    
                    **Success Rate:** {treatment_plan['success_rate']}%
                    
                    **Est. Cost:** ₹{treatment_plan['cost_estimate']:,}
                    """)
    
    # Environmental Factors
    st.subheader("🌡️ Environmental Assessment")
    
    env_factors = analysis_report['environmental_factors']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Current Season:** {env_factors['season']}")
        st.write(f"**Risk Level:** {env_factors['risk_level']}")
    
    with col2:
        st.write("**Risk Factors:**")
        for factor in env_factors['risk_factors']:
            st.write(f"• {factor}")
    
    # Prevention Strategies
    st.subheader("🛡️ Prevention Strategies")
    
    prevention = disease_detector.get_prevention_strategies(crop_type, location)
    
    with st.expander("📅 Seasonal Management Calendar", expanded=False):
        for stage, activities in prevention['seasonal_calendar'].items():
            st.write(f"**{stage}**")
            for activity in activities:
                st.write(f"• {activity}")
            st.write("")
    
    with st.expander("📝 Weekly Monitoring Checklist", expanded=False):
        for item in prevention['monitoring_checklist']:
            st.write(item)
    
    # Expert Consultation
    st.subheader("👨‍🌾 Expert Consultation")
    
    consultation = disease_detector.generate_expert_consultation_request(analysis_report)
    
    if consultation['needed']:
        st.warning("🔔 **Expert consultation recommended for this case**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Key Concerns:**")
            for concern in consultation['key_concerns']:
                st.write(f"• {concern}")
        
        with col2:
            st.info(f"""
            **Consultation Details**
            
            **Priority:** {consultation['priority']}
            
            **Est. Fee:** ₹{consultation['estimated_consultation_fee']}
            
            **Recommended Experts:** {', '.join(consultation['recommended_expert_types'])}
            """)
        
        if st.button("📞 Request Expert Consultation"):
            st.success("✅ Consultation request sent! An expert will contact you within 24 hours.")
    else:
        st.success("✅ Current analysis is sufficient for management. No expert consultation needed.")

def run_demo_analysis(demo_data, disease_detector):
    """Run a demo analysis with predefined data."""
    
    st.subheader(f"🎬 Demo: {demo_data['crop']} Disease Analysis")
    
    with st.spinner("Running demo analysis..."):
        # Simulate analysis for demo
        import time
        time.sleep(2)
        
        # Create mock analysis report
        mock_diseases = [{
            'disease_id': demo_data['disease'],
            'name': disease_detector.disease_database[demo_data['disease']]['name'],
            'severity': demo_data['severity'],
            'confidence': 0.89
        }]
        
        analysis_report = {
            'confidence_score': 0.89,
            'image_quality': {'score': 'Good', 'feedback': 'Good image quality for demo'},
            'urgency_level': 'Medium' if demo_data['severity'] == 'moderate' else 'Low',
            'diseases_detected': mock_diseases,
            'environmental_factors': {
                'season': 'Monsoon',
                'risk_level': 'Medium',
                'risk_factors': ['High humidity', 'Excessive moisture']
            }
        }
    
    st.success("✅ Demo Analysis Complete!")
    
    # Show demo results (simplified version)
    disease = mock_diseases[0]
    treatment_plan = disease_detector.get_treatment_plan(
        disease['disease_id'], disease['severity'], demo_data['crop']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **🦠 Detected Disease**
        
        **Name:** {disease['name']}
        
        **Severity:** {disease['severity'].title()}
        
        **Confidence:** {disease['confidence']:.0%}
        """)
    
    with col2:
        st.warning(f"""
        **💊 Treatment Summary**
        
        **Timeline:** {treatment_plan['timeline']}
        
        **Success Rate:** {treatment_plan['success_rate']}%
        
        **Est. Cost:** ₹{treatment_plan['cost_estimate']:,}
        """)
    
    st.write("**🏥 Immediate Actions:**")
    for action in treatment_plan['immediate_actions']:
        st.write(f"• {action}")

def show_disease_education(disease_detector):
    """Display educational content about crop diseases."""
    
    st.subheader("📚 Learn About Crop Diseases")
    
    with st.expander("🦠 Common Crop Diseases Database"):
        
        for disease_id, disease_info in disease_detector.disease_database.items():
            st.write(f"**{disease_info['name']}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("*Affected Crops:*")
                st.write(", ".join(disease_info['crops_affected']))
                
                st.write("*Symptoms:*")
                for symptom in disease_info['symptoms']:
                    st.write(f"• {symptom}")
            
            with col2:
                st.write("*Causes:*")
                for cause in disease_info['causes']:
                    st.write(f"• {cause}")
                
                st.write("*Prevention:*")
                for prevention in disease_info['prevention'][:3]:  # Show first 3
                    st.write(f"• {prevention}")
            
            st.write("---")
    
    with st.expander("💡 Pro Tips for Disease Management"):
        tips = [
            "🔍 **Early Detection**: Check your crops weekly for any unusual symptoms",
            "📸 **Photo Documentation**: Keep records of disease progression with photos", 
            "🌡️ **Weather Monitoring**: Track conditions favorable for disease development",
            "🧹 **Field Hygiene**: Remove infected plant debris immediately",
            "💊 **Preventive Treatment**: Apply fungicides before disease pressure builds",
            "👨‍🌾 **Expert Consultation**: Don't hesitate to consult experts for severe cases",
            "📱 **Technology Use**: Leverage AI tools like this for quick identification",
            "📝 **Record Keeping**: Maintain treatment logs for future reference"
        ]
        
        for tip in tips:
            st.write(tip)

if __name__ == "__main__":
    main()