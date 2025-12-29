import streamlit as st
import pandas as pd
import xgboost
import numpy as np

# Page configuration - sidebar collapsed by default
st.set_page_config(
    page_title="Predict Risk - HeartGuard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Clean Sidebar with Vibrant Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #2d1f3d 100%) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] a {
        color: #ff8fab !important;
    }
    
    /* Page Title */
    .page-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 50%, #ffc3d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        color: #cccccc;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ff8fab;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255, 107, 156, 0.3);
    }
    
    /* Result Cards */
    .result-card-safe {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.2) 0%, rgba(0, 200, 150, 0.1) 100%);
        border: 3px solid #00ffaa;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 15px 50px rgba(0, 255, 170, 0.3);
    }
    
    .result-card-risk {
        background: linear-gradient(135deg, rgba(255, 87, 87, 0.2) 0%, rgba(255, 140, 66, 0.1) 100%);
        border: 3px solid #ff5757;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 15px 50px rgba(255, 87, 87, 0.3);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .result-title-safe {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffaa;
        margin-bottom: 0.5rem;
    }
    
    .result-title-risk {
        font-size: 2rem;
        font-weight: 800;
        color: #ff5757;
        margin-bottom: 0.5rem;
    }
    
    .result-message {
        font-size: 1.1rem;
        color: #e0e0e0;
    }
    
    /* CTA Button */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(255, 107, 156, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 156, 0.5) !important;
    }
    
    /* Warning Box */
    .warning-box {
        background: rgba(255, 180, 0, 0.15);
        border: 1px solid rgba(255, 180, 0, 0.4);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0 2rem 0;
    }
    
    /* Make ALL form labels bright white */
    .stNumberInput label,
    .stSelectbox label,
    .stSlider label,
    .stTextInput label,
    .stRadio label,
    label,
    .stNumberInput > label,
    .stSelectbox > label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Help text */
    .stNumberInput small,
    .stSelectbox small,
    .stSlider small {
        color: #aaaaaa !important;
    }
    
    /* Style the header to be dark */
    header[data-testid="stHeader"] {
        background: #0f0f1a !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Make sidebar toggle arrow white */
    button[data-testid="stBaseButton-headerNoPadding"] {
        color: #ffffff !important;
    }
    
    button[data-testid="stBaseButton-headerNoPadding"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    model = xgboost.Booster()
    model.load_model('xgb_model.bin')
    return model

loaded_model = load_model()

# Sidebar Content
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 2rem; margin: 0;">🔬</p>
        <h2 style="color: #ff8fab; margin: 0.5rem 0;">Risk Predictor</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">📋 How It Works</p>
        <ol style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.8;">
            <li>Enter your clinical parameters</li>
            <li>AI analyzes 7 key factors</li>
            <li>Get instant risk assessment</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">🤖 Model Info</p>
        <p style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.6;">
        <strong>Algorithm:</strong> XGBoost<br>
        <strong>Accuracy:</strong> ~85%<br>
        <strong>Features:</strong> 7 clinical parameters
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Dashboard.py")

# Page Header
st.markdown('<h1 class="page-title">🔬 Heart Disease Risk Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Enter your clinical parameters to assess your heart disease risk</p>', unsafe_allow_html=True)

# Warning
st.markdown("""
<div class="warning-box">
    <p style="color: #ffcc00; margin: 0; font-weight: 500; text-align: center;">
    ⚠️ <strong>Disclaimer:</strong> This is NOT a medical diagnosis. Always consult a healthcare provider.</p>
</div>
""", unsafe_allow_html=True)

# Create clean form layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">👤 Basic Information</div>', unsafe_allow_html=True)
    
    age = st.number_input('Age (years)', min_value=1, max_value=120, value=45, step=1,
                          help="Your current age")
    
    sex = st.selectbox('Biological Sex', ('Male', 'Female'))
    sex_val = 1 if sex == 'Male' else 0
    
    st.markdown('<div class="section-header">❤️ Heart Measurements</div>', unsafe_allow_html=True)
    
    trtbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=80, max_value=250, value=120, step=1,
                              help="Normal: <120 mm Hg")
    
    chol = st.slider('Cholesterol Level (mg/dl)', min_value=100, max_value=600, value=200, step=5,
                     help="Desirable: <200 mg/dl")
    
    thalachh = st.slider('Maximum Heart Rate', min_value=60, max_value=220, value=150, step=1,
                         help="Estimate: 220 - your age")

with col2:
    st.markdown('<div class="section-header">🩺 Clinical Symptoms</div>', unsafe_allow_html=True)
    
    cp_options = {
        'Asymptomatic (No chest pain)': 0,
        'Atypical Angina': 1,
        'Non-Anginal Pain': 2,
        'Typical Angina': 3
    }
    cp = st.selectbox('Chest Pain Type', list(cp_options.keys()))
    cp_val = cp_options[cp]
    
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl?', ('No', 'Yes'))
    fbs_val = 1 if fbs == 'Yes' else 0
    
    exng = st.selectbox('Exercise-Induced Angina?', ('No', 'Yes'))
    exng_val = 1 if exng == 'Yes' else 0
    
    st.markdown('<div class="section-header">📊 ECG & Test Results</div>', unsafe_allow_html=True)
    
    restecg_options = {
        'Normal': 0,
        'ST-T Wave Abnormality': 1,
        'Left Ventricular Hypertrophy': 2
    }
    restecg = st.selectbox('Resting ECG Results', list(restecg_options.keys()))
    restecg_val = restecg_options[restecg]
    
    oldpeak = st.slider('ST Depression (Oldpeak)', min_value=0.0, max_value=6.0, value=1.0, step=0.1)

# Additional parameters
st.markdown('<div class="section-header">🔎 Additional Factors</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    slope_options = {'Downsloping': 0, 'Flat': 1, 'Upsloping': 2}
    slp = st.selectbox('Peak Exercise ST Slope', list(slope_options.keys()))
    slp_val = slope_options[slp]

with col2:
    caa = st.selectbox('Major Vessels (0-3)', (0, 1, 2, 3))

with col3:
    thall_options = {'Normal': 2, 'Fixed Defect': 1, 'Reversible Defect': 3, 'Unknown': 0}
    thall = st.selectbox('Thalassemia', list(thall_options.keys()))
    thall_val = thall_options[thall]

# Predict Button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    predict_clicked = st.button('🔬 Analyze My Heart Risk', use_container_width=True)

# Prediction Logic
if predict_clicked:
    features_values = {'age': age, 'trtbps': trtbps, 'chol': chol, 'thalachh': thalachh}
    
    if any(value == 0 for value in features_values.values()):
        st.warning('⚠️ Please fill in all required fields with valid values.')
    else:
        data = pd.DataFrame({
            'thall': [thall_val],
            'caa': [caa],
            'cp': [cp_val],
            'oldpeak': [oldpeak],
            'exng': [exng_val],
            'chol': [chol],
            'thalachh': [thalachh]
        })
        
        dtest = xgboost.DMatrix(data)
        
        # Extended loading animation (2.5 seconds)
        import time
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            ("🔄 Preparing your data...", 0.3),
            ("🧠 Running AI analysis...", 0.6),
            ("📊 Calculating risk factors...", 0.8),
            ("✨ Generating results...", 1.0)
        ]
        
        for text, progress in stages:
            status_text.markdown(f"<p style='text-align: center; color: #ff8fab; font-size: 1.1rem;'>{text}</p>", unsafe_allow_html=True)
            progress_bar.progress(progress)
            time.sleep(0.6)
        
        status_text.empty()
        progress_bar.empty()
        
        prediction_prob = loaded_model.predict(dtest)[0]
        prediction = 1 if prediction_prob >= 0.5 else 0
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if prediction == 0:
            st.markdown("""
            <div class="result-card-safe">
                <div class="result-icon">💚</div>
                <div class="result-title-safe">Low Risk Detected</div>
                <div class="result-message">Based on the parameters provided, you appear to have a <strong>lower risk</strong> of heart disease.</div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            st.success("✅ Continue maintaining a healthy lifestyle and get regular check-ups!")
        else:
            st.markdown("""
            <div class="result-card-risk">
                <div class="result-icon">⚠️</div>
                <div class="result-title-risk">Elevated Risk Detected</div>
                <div class="result-message">Based on the parameters provided, you may have an <strong>elevated risk</strong> of heart disease.</div>
            </div>
            """, unsafe_allow_html=True)
            st.error("🏥 **Please consult a healthcare professional for proper evaluation.**")
        
        st.markdown("---")
        confidence = abs(0.5 - prediction_prob) * 200
        st.caption(f"Model Confidence: {confidence:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>🫀 Heart Attack Prediction System | XGBoost ML Model</p>
    <p style="font-size: 0.8rem;">Final Year Major Project</p>
</div>
""", unsafe_allow_html=True)
