"""
AI-Powered Crop Disease Detection - Standalone Page

Complete disease detection system with camera capture, file upload,
multi-image analysis, and treatment recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import random
from pathlib import Path
from PIL import Image
from datetime import datetime
import hashlib

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import required modules
from src.core.data_loader import DataLoader
from features.crop_disease_detector import CropDiseaseDetector

# Page configuration
st.set_page_config(
    page_title="🔬 Disease Detection - FasalMitra",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize session state for disease tracking."""
    if 'disease_history' not in st.session_state:
        st.session_state.disease_history = []
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    if 'user_location' not in st.session_state:
        st.session_state.user_location = ""

initialize_session_state()

# Load data and initialize detector
@st.cache_resource
def load_disease_detector():
    """Load and cache the disease detector."""
    try:
        data_loader = DataLoader(str(project_root))
        data_loader.load_datasets()
        disease_detector = CropDiseaseDetector(data_loader)
        return disease_detector
    except Exception as e:
        st.error(f"Error initializing disease detector: {e}")
        return None

disease_detector = load_disease_detector()

if not disease_detector:
    st.error("Failed to initialize disease detector. Please check the data files.")
    st.stop()

# ========== Helper Functions (Copied from streamlit_app.py) ==========

def show_disease_progression_timeline():
    """Display disease analysis history timeline."""
    if not hasattr(st.session_state, 'disease_history') or not st.session_state.disease_history:
        return
    
    st.markdown("### 📊 Analysis Timeline")
    
    # Show recent analyses in reverse chronological order
    for i, entry in enumerate(reversed(st.session_state.disease_history[-5:])):  # Last 5 entries
        with st.expander(f"Analysis {len(st.session_state.disease_history) - i} - {entry['timestamp']}", expanded=(i==0)):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if 'crop' in entry:
                    st.metric("Crop", entry['crop'])
                if 'disease' in entry:
                    st.metric("Disease", entry['disease'])
                if 'severity' in entry:
                    severity_color = {"mild": "🟢", "moderate": "🟡", "severe": "🔴"}.get(entry['severity'], "⚪")
                    st.metric("Severity", f"{severity_color} {entry['severity'].title()}")
            
            with col2:
                if 'confidence' in entry:
                    st.progress(entry['confidence'] / 100)
                    st.caption(f"Confidence: {entry['confidence']}%")
                
                if 'treatment_summary' in entry:
                    st.markdown(f"**Treatment:** {entry['treatment_summary']}")


def run_enhanced_demo_analysis(demo_data, disease_detector, location):
    """Run demo analysis with simulated data."""
    with st.spinner("🔬 Running demo analysis..."):
        # Create simulated analysis result manually
        crop = demo_data['crop']
        disease_id = demo_data['disease']
        severity = demo_data['severity']
        
        # Build result based on disease database
        if disease_id == 'healthy':
            result = {
                'disease_name': 'Healthy',
                'severity': 'none',
                'confidence': 95,
                'symptoms': [],
                'causes': [],
                'treatments': [],
                'prevention': ['Continue regular monitoring', 'Maintain proper irrigation'],
                'cost_estimate': 0,
                'primary_treatment': 'No treatment required'
            }
        else:
            # Get disease info from database
            disease_info = disease_detector.disease_database.get(disease_id, {})
            
            result = {
                'disease_name': disease_info.get('name', 'Unknown Disease'),
                'severity': severity,
                'confidence': random.randint(80, 95),
                'symptoms': disease_info.get('symptoms', []),
                'causes': disease_info.get('causes', []),
                'treatments': disease_info.get('treatments', {}).get(severity, []),
                'prevention': disease_info.get('prevention', []),
                'cost_estimate': disease_info.get('cost_estimate', {}).get(severity, 0),
                'application_method': 'Apply as foliar spray, covering both sides of leaves. Repeat every 7-10 days.',
                'primary_treatment': disease_info.get('treatments', {}).get(severity, ['No treatment'])[0] if disease_info.get('treatments', {}).get(severity) else 'No treatment'
            }
        
        if location:
            result['location'] = location
        
        # Display results
        display_enhanced_analysis_results(result, crop, location, is_demo=True)


def show_disease_education(disease_detector):
    """Show educational content about diseases."""
    st.markdown("---")
    st.markdown("### 📚 Disease Information Center")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🌾 Common Crop Diseases
        
        **Fungal Diseases:**
        - **Leaf Spot** - Brown/black spots on leaves
        - **Rust** - Orange/brown pustules
        - **Blight** - Rapid wilting and browning
        - **Powdery Mildew** - White powdery coating
        
        **Bacterial Diseases:**
        - **Bacterial Blight** - Water-soaked lesions
        - **Wilt** - Plant wilting despite adequate water
        
        **Viral Diseases:**
        - **Mosaic Virus** - Mottled yellow/green patterns
        - **Leaf Curl** - Distorted, curled leaves
        """)
    
    with col2:
        st.markdown("""
        #### 💡 Prevention Tips
        
        **Field Management:**
        - Crop rotation (3-4 year cycle)
        - Proper spacing for air circulation
        - Remove plant debris after harvest
        - Use disease-free seeds
        
        **Water Management:**
        - Avoid overhead irrigation
        - Water in morning hours
        - Ensure proper drainage
        
        **Regular Monitoring:**
        - Weekly field inspections
        - Early detection is key
        - Document disease progression
        - Consult agriculture experts
        """)
    
    # Best Practices Section
    with st.expander("🎯 Best Practices for Disease Management", expanded=False):
        st.markdown("""
        **Integrated Pest Management (IPM) Approach:**
        
        1. **Cultural Control:**
           - Crop rotation with non-host crops
           - Use resistant varieties
           - Proper plant spacing and pruning
           - Field sanitation
        
        2. **Biological Control:**
           - Use beneficial microorganisms
           - Natural predators for pest control
           - Compost and organic matter
        
        3. **Chemical Control (Last Resort):**
           - Use only when necessary
           - Follow recommended dosage
           - Rotate fungicides to prevent resistance
           - Observe pre-harvest intervals
        
        4. **Monitoring & Record Keeping:**
           - Regular field inspections
           - Document disease occurrence
           - Track treatment effectiveness
           - Weather-based disease forecasting
        """)
    
    # IPM Strategy Recommendations
    with st.expander("📋 Recommended IPM Strategies by Crop", expanded=False):
        ipm_strategies = {
            "Rice": [
                "Flood irrigation to control weeds",
                "Use pheromone traps for stem borers",
                "Apply bio-pesticides like Trichoderma",
                "Rotate with upland crops"
            ],
            "Wheat": [
                "Crop rotation with legumes",
                "Use disease-resistant varieties",
                "Timely sowing to avoid rust",
                "Zinc application for disease tolerance"
            ],
            "Cotton": [
                "Intercropping with cereals or legumes",
                "Use pink bollworm pheromone traps",
                "Neem-based sprays for sucking pests",
                "Remove crop residues post-harvest"
            ],
            "Tomato": [
                "Drip irrigation to reduce humidity",
                "Stake plants for better air circulation",
                "Use bio-fungicides preventively",
                "Remove infected plants immediately"
            ]
        }
        
        for crop, strategies in ipm_strategies.items():
            st.markdown(f"**{crop}:**")
            for strategy in strategies:
                st.markdown(f"• {strategy}")


def display_enhanced_analysis_results(analysis, crop_type, location, is_demo=False):
    """Display comprehensive analysis results with all features."""
    
    # Store in history
    if not hasattr(st.session_state, 'disease_history'):
        st.session_state.disease_history = []
    
    history_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'crop': crop_type,
        'disease': analysis.get('disease_name', 'Unknown'),
        'severity': analysis.get('severity', 'unknown'),
        'confidence': int(analysis.get('confidence', 0)),
        'treatment_summary': analysis.get('primary_treatment', 'No treatment recommended')
    }
    st.session_state.disease_history.append(history_entry)
    st.session_state.analysis_count = len(st.session_state.disease_history)
    
    # Display results
    if is_demo:
        st.info("🎮 **Demo Analysis** - This is a simulated result for demonstration")
    
    st.success("✅ **Analysis Complete!**")
    
    # Basic Information
    st.markdown("### 🔍 Detection Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌾 Crop Type", crop_type)
    
    with col2:
        disease_name = analysis.get('disease_name', 'Healthy')
        st.metric("🦠 Disease Detected", disease_name)
    
    with col3:
        severity = analysis.get('severity', 'none')
        severity_emoji = {"mild": "🟢", "moderate": "🟡", "severe": "🔴", "none": "✅"}.get(severity, "⚪")
        st.metric("📊 Severity", f"{severity_emoji} {severity.title()}")
    
    with col4:
        confidence = analysis.get('confidence', 0)
        st.metric("🎯 Confidence", f"{confidence}%")
    
    # Confidence indicator
    st.progress(confidence / 100)
    
    # Detailed Analysis
    if analysis.get('disease_name') != 'Healthy':
        st.markdown("---")
        st.markdown("### 📋 Detailed Analysis")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔬 Symptoms", "💊 Treatment", "💰 Cost Estimate", "🎓 Prevention"])
        
        with tab1:
            st.markdown("#### Observed Symptoms")
            symptoms = analysis.get('symptoms', [])
            if symptoms:
                for symptom in symptoms:
                    st.markdown(f"• {symptom}")
            else:
                st.info("No specific symptoms identified")
            
            causes = analysis.get('causes', [])
            if causes:
                st.markdown("#### Possible Causes")
                for cause in causes:
                    st.markdown(f"• {cause}")
        
        with tab2:
            st.markdown("#### Recommended Treatment")
            
            treatments = analysis.get('treatments', [])
            if treatments:
                for i, treatment in enumerate(treatments, 1):
                    st.markdown(f"**{i}.** {treatment}")
            else:
                st.info("No specific treatment required")
            
            if analysis.get('application_method'):
                st.markdown("#### Application Method")
                st.info(analysis['application_method'])
        
        with tab3:
            st.markdown("#### Treatment Cost Estimate")
            
            cost = analysis.get('cost_estimate', 0)
            st.metric("Estimated Cost", f"₹{cost:,.0f}")
            
            st.markdown("""
            *Cost includes:*
            - Fungicides/Pesticides
            - Labor
            - Equipment/Spraying costs
            - Additional treatments (if needed)
            
            *Note: Costs may vary by region and availability*
            """)
        
        with tab4:
            st.markdown("#### Prevention Measures")
            
            prevention = analysis.get('prevention', [])
            if prevention:
                for measure in prevention:
                    st.markdown(f"• {measure}")
            else:
                st.info("Follow general crop management practices")
    else:
        st.success("🎉 **Healthy Plant Detected!** No disease symptoms found.")
        st.markdown("""
        **Maintenance Tips:**
        - Continue regular monitoring
        - Maintain proper irrigation
        - Ensure good air circulation
        - Use preventive treatments as needed
        """)


def analyze_enhanced_crop_disease(photos_data, crop_type, location, disease_detector):
    """Enhanced analysis with multiple photos."""
    
    with st.spinner(f"🔬 Analyzing {len(photos_data)} photo(s)..."):
        
        all_analyses = []
        invalid_images = []
        
        for source, photo in photos_data:
            image_data = photo.read()
            
            analysis = disease_detector.analyze_image(image_data, crop_type, location)
            analysis['source'] = source
            
            if not analysis.get('is_valid_crop_image', True):
                invalid_images.append((source, analysis))
            else:
                all_analyses.append(analysis)
        
        if not all_analyses:
            st.error("**No Valid Crop Images Detected**")
            st.markdown("### Please upload photos of actual crops, plants, or leaves.")
            return
        
        if invalid_images:
            st.warning(f"⚠️ **{len(invalid_images)} out of {len(photos_data)} images were not valid crop images.**")
    
    if len(all_analyses) == 1:
        aggregated_analysis = all_analyses[0]
        st.success("✅ **Analysis Complete!**")
    else:
        aggregated_analysis = disease_detector.aggregate_multi_photo_analysis(all_analyses)
        st.success(f"✅ **Multi-Photo Analysis Complete!** Analyzed {len(all_analyses)} images.")
    
    # Display results
    display_enhanced_analysis_results(aggregated_analysis, crop_type, location)


# ========== Main Disease Detection Interface ==========

def show_disease_detection_page():
    """Main disease detection interface."""
    
    st.title("🔬 AI-Powered Crop Disease Detection")
    st.markdown("*Upload or capture photos for AI-powered disease analysis and treatment recommendations*")
    
    # Disease progression tracking display
    if st.session_state.disease_history:
        with st.expander(f"📊 Analysis History ({len(st.session_state.disease_history)} previous analyses)", expanded=False):
            show_disease_progression_timeline()
    
    # Image capture/upload section
    st.markdown("---")
    st.subheader("📤 Image Upload Options")
    
    tab1, tab2 = st.tabs(["📸 Camera Capture", "📁 File Upload"])
    
    camera_photo = None
    uploaded_files = None
    
    with tab1:
        st.markdown("**Real-time Camera Capture**")
        
        st.info("📸 Make sure your browser supports camera access and you're on a secure connection (HTTPS or localhost)")
        
        with st.expander("🔧 Camera Not Working? Troubleshooting Tips", expanded=False):
            st.write("""
            **If camera permission is not requested:**
            - Refresh the page (Ctrl+F5)
            - Check browser address bar for camera icon 🎥
            - Try in Chrome or Firefox
            - Make sure no other apps are using your camera
            - Check browser settings: Allow camera for this site
            - Clear browser cache and try again
            """)
        
        camera_photo = st.camera_input(
            "📸 Click here to activate camera and take a photo of your crop",
            key="disease_detection_camera",
            help="Your browser will request camera permission when you interact with this camera widget"
        )
        
        if camera_photo:
            st.success("✅ Photo captured successfully!")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(camera_photo, caption="Camera Preview", width=200)
    
    with tab2:
        st.markdown("**📁 Upload Crop Photos**")
        
        uploaded_files = st.file_uploader(
            "Choose crop images...",
            type=['png', 'jpg', 'jpeg', 'webp'],
            accept_multiple_files=True,
            help="Upload one or more images of affected crops"
        )
        
        if uploaded_files:
            st.success(f"✅ **{len(uploaded_files)} photo(s) ready for analysis**")
            
            if len(uploaded_files) <= 3:
                preview_cols = st.columns(len(uploaded_files))
                for i, file in enumerate(uploaded_files):
                    with preview_cols[i]:
                        st.image(file, caption=f"📷 Image {i+1}", width=150)
    
    # Prepare photos for analysis
    photos_to_analyze = []
    crop_type = "Auto-Detect"
    location = st.session_state.get('user_location', "")
    
    if camera_photo:
        photos_to_analyze.append(("Camera", camera_photo))
    if uploaded_files:
        for i, file in enumerate(uploaded_files):
            photos_to_analyze.append((f"Upload-{i+1}", file))
    
    # Analysis section
    if photos_to_analyze:
        st.markdown("---")
        st.subheader(f"🔬 Analysis Ready ({len(photos_to_analyze)} photos)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🔬 Run Analysis", type="primary", use_container_width=True):
                analyze_enhanced_crop_disease(photos_to_analyze, crop_type, location, disease_detector)
        with col2:
            st.info(f"{len(photos_to_analyze)} image(s) ready")
    
    else:
        # Demo section
        st.markdown("---")
        st.subheader("🎮 Demo Analysis")
        
        demo_scenarios = {
            "Rice Leaf Spot (Moderate)": {"crop": "Rice", "disease": "leaf_spot", "severity": "moderate"},
            "Wheat Rust Disease (Mild)": {"crop": "Wheat", "disease": "rust_disease", "severity": "mild"},
            "Cotton Bacterial Blight (Severe)": {"crop": "Cotton", "disease": "bacterial_blight", "severity": "severe"},
            "Healthy Plant (No Disease)": {"crop": "Tomato", "disease": "healthy", "severity": "none"},
        }
        
        selected_demo = st.selectbox("Select a demo scenario:", list(demo_scenarios.keys()))
        
        if st.button("▶️ Run Demo Analysis", use_container_width=True):
            demo_data = demo_scenarios[selected_demo]
            run_enhanced_demo_analysis(demo_data, disease_detector, location)
    
    # Educational content
    st.markdown("---")
    show_disease_education(disease_detector)


# ========== Sidebar ==========

with st.sidebar:
    st.markdown("## 🔬 Disease Detection")
    
    st.info("""
    **Features:**
    - 📸 Real-time camera capture
    - 📁 Multi-image upload
    - 🤖 AI-powered analysis
    - 💊 Treatment recommendations
    - 💰 Cost estimates
    - 📊 Analysis history
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Session Stats")
    st.metric("Total Analyses", st.session_state.analysis_count)
    
    if st.session_state.disease_history:
        latest = st.session_state.disease_history[-1]
        st.metric("Latest Detection", latest.get('disease', 'N/A'))
        st.metric("Latest Severity", latest.get('severity', 'N/A').title())
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")
    
    st.markdown("---")
    st.caption("Powered by AI & Computer Vision")

# ========== Run Main App ==========

show_disease_detection_page()
