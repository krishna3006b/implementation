import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About - HeartGuard",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
    
    /* Sidebar */
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
    
    /* Section Headers - BRIGHT WHITE */
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff !important;
        margin: 2rem 0 1rem 0;
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, rgba(255, 107, 156, 0.1) 0%, rgba(138, 43, 226, 0.08) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 107, 156, 0.2);
        margin-bottom: 1rem;
    }
    
    .info-card p {
        color: #ffffff !important;
        line-height: 1.8;
    }
    
    /* Tech Badges */
    .tech-badge {
        display: inline-block;
        background: rgba(255, 107, 156, 0.2);
        border: 1px solid rgba(255, 107, 156, 0.4);
        border-radius: 20px;
        padding: 0.4rem 0.8rem;
        margin: 0.3rem;
        color: #ff8fab;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Model Card */
    .model-card {
        background: rgba(74, 144, 226, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid #4a90e2;
    }
    
    .model-card h4 {
        color: #6bb3ff;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Header dark */
    header[data-testid="stHeader"] {
        background: #0f0f1a !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Sidebar toggle white */
    button[data-testid="stBaseButton-headerNoPadding"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    /* Hide branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar Content
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 2rem; margin: 0;">ℹ️</p>
        <h2 style="color: #ff8fab; margin: 0.5rem 0;">About</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">🎓 Project Details</p>
        <p style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.6;">
        <strong>Type:</strong> Final Year Major Project<br>
        <strong>Topic:</strong> Heart Attack Prediction using ML<br>
        <strong>Algorithm:</strong> Logistic Regression
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">🔗 Quick Links</p>
        <ul style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.8;">
            <li>UCI Dataset</li>
            <li>Scikit-learn Docs</li>
            <li>Streamlit Docs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Dashboard.py")

# Page Header
st.markdown('<h1 class="page-title">ℹ️ About This Project</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Heart Attack Prediction using Machine Learning</p>', unsafe_allow_html=True)

# Project Overview
st.markdown('<h2 class="section-title">🎯 Project Overview</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="info-card">
    <p><strong style="color: #ff8fab;">HeartGuard</strong> is a machine learning-based heart attack prediction system 
    developed as a <strong>Final Year Major Project</strong>. The system uses clinical parameters to predict the 
    likelihood of heart disease, helping in early detection and prevention.</p>
    <p style="color: #aaa; margin-top: 1rem;">This project demonstrates the practical application of 
    <strong style="color: #ff8fab;">Machine Learning in Healthcare</strong> for disease prediction and awareness.</p>
</div>
""", unsafe_allow_html=True)

# Objectives
st.markdown('<h2 class="section-title">🎯 Project Objectives</h2>', unsafe_allow_html=True)
st.info("""
**Primary Objectives:**
1. To develop a machine learning model for heart attack prediction
2. To create an interactive web application for risk assessment
3. To raise awareness about cardiovascular health in India
4. To demonstrate ML application in healthcare domain
""")

# Technology Stack
st.markdown('<h2 class="section-title">🛠️ Technology Stack</h2>', unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <span class="tech-badge">🐍 Python 3.x</span>
    <span class="tech-badge">🚀 Streamlit</span>
    <span class="tech-badge">🤖 Logistic Regression</span>
    <span class="tech-badge">📊 Pandas</span>
    <span class="tech-badge">🔢 NumPy</span>
    <span class="tech-badge">📈 Scikit-learn</span>
</div>
""", unsafe_allow_html=True)

# Model Details
st.markdown('<h2 class="section-title">🧠 Machine Learning Model</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="model-card">
        <h4>📊 Model Specifications</h4>
        <ul style="color: #e0e0e0; line-height: 2.2;">
            <li><strong>Algorithm:</strong> Logistic Regression</li>
            <li><strong>Training Data:</strong> 303 patients</li>
            <li><strong>Features:</strong> 7 clinical parameters</li>
            <li><strong>Accuracy:</strong> ~85%</li>
            <li><strong>AUC Score:</strong> ~0.87</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="model-card">
        <h4>🔬 Features Used</h4>
        <ul style="color: #e0e0e0; line-height: 2.2;">
            <li><strong>Thalassemia</strong> - Blood disorder type</li>
            <li><strong>Major Vessels</strong> - Count via fluoroscopy</li>
            <li><strong>Chest Pain Type</strong> - Clinical symptom</li>
            <li><strong>ST Depression</strong> - ECG parameter</li>
            <li><strong>Exercise Angina</strong> - Symptom indicator</li>
            <li><strong>Cholesterol</strong> - Blood lipid level</li>
            <li><strong>Max Heart Rate</strong> - Peak rate achieved</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Methodology
st.markdown('<h2 class="section-title">📋 Methodology</h2>', unsafe_allow_html=True)
st.markdown("""
<div style="color: #ffffff; line-height: 2; font-size: 1rem;">
<p style="color: #ff8fab; font-weight: 600; margin-bottom: 1rem;">Development Process:</p>
<ol style="color: #ffffff;">
    <li><strong>Data Collection</strong> - UCI Heart Disease Dataset (Cleveland Database)</li>
    <li><strong>Data Preprocessing</strong> - Cleaning, handling missing values</li>
    <li><strong>Exploratory Data Analysis</strong> - Understanding patterns and correlations</li>
    <li><strong>Feature Selection</strong> - Identifying most predictive features using Mutual Information</li>
    <li><strong>Model Training</strong> - Logistic Regression with cross-validation and calibration checks</li>
    <li><strong>Hyperparameter Tuning</strong> - Optimizing model parameters</li>
    <li><strong>Evaluation</strong> - Using accuracy, AUC score, and cross-validation</li>
    <li><strong>Deployment</strong> - Web application using Streamlit framework</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Dataset
st.markdown('<h2 class="section-title">📚 Dataset Information</h2>', unsafe_allow_html=True)
st.info("""
**Heart Disease Dataset (UCI Machine Learning Repository)**

- **Source:** Cleveland Database, UCI Repository
- **Total Samples:** 303 patient records
- **Features:** 13 clinical attributes + 1 target variable
- **Target Variable:** Presence (1) or Absence (0) of heart disease
- **Attributes:** Age, Sex, Chest Pain, Blood Pressure, Cholesterol, ECG, Max Heart Rate, etc.
""")

# India Context
st.markdown('<h2 class="section-title">🇮🇳 Relevance to India</h2>', unsafe_allow_html=True)
st.success("""
**Why Heart Attack Prediction Matters for India:**

- **2.8 million** Indians die from heart disease every year
- Indians experience heart attacks **10 years earlier** than global average
- **28%** of all deaths in India are due to cardiovascular diseases
- **80%** of heart attacks are preventable with early detection
- Awareness tools like this can encourage early screening and lifestyle changes
""")

# Disclaimer
st.markdown('<h2 class="section-title">⚠️ Disclaimer</h2>', unsafe_allow_html=True)
st.error("""
**Important Notice:**

This application is developed for **educational and research purposes** as part of an academic project.
- It is NOT a substitute for professional medical diagnosis
- Results should NOT be used for making medical decisions
- Always consult qualified healthcare professionals for health concerns
""")

# References
st.markdown('<h2 class="section-title">📖 References</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="color: #ffffff; line-height: 2;">
        <p style="color: #ff8fab; font-weight: 600;">Data Sources:</p>
        <ul style="color: #ffffff;">
            <li>UCI Machine Learning Repository</li>
            <li>Cleveland Heart Disease Database</li>
        </ul>
        <p style="color: #ff8fab; font-weight: 600; margin-top: 1rem;">Health Data:</p>
        <ul style="color: #ffffff;">
            <li>Indian Council of Medical Research (ICMR)</li>
            <li>World Health Organization (WHO)</li>
            <li>Indian Heart Association</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="color: #ffffff; line-height: 2;">
        <p style="color: #ff8fab; font-weight: 600;">Technical References:</p>
        <ul style="color: #ffffff;">
            <li>Logistic Regression (Scikit-learn)</li>
            <li>Streamlit Documentation</li>
            <li>Scikit-learn Documentation</li>
        </ul>
        <p style="color: #ff8fab; font-weight: 600; margin-top: 1rem;">Research Papers:</p>
        <ul style="color: #ffffff;">
            <li>Heart Disease Prediction using ML techniques</li>
            <li>Comparative analysis of classification algorithms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; color: #888;">
    <p style="font-size: 1.1rem; font-weight: 600;">🫀 HeartGuard - Heart Attack Prediction System</p>
    <p style="font-size: 0.95rem;">Final Year Major Project | Machine Learning in Healthcare</p>
    <p style="font-size: 0.85rem; color: #666;">© 2024-2025</p>
</div>
""", unsafe_allow_html=True)
