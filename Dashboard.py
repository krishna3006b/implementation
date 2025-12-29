import streamlit as st

# Page configuration - sidebar collapsed by default
st.set_page_config(
    page_title="HeartGuard - Heart Disease Awareness",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar collapsed by default
)

# Custom CSS for stunning UI with vibrant colors
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles - Clean Dark Theme */
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
    
    /* Sidebar text - bright white */
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #ffffff !important;
    }
    
    /* Sidebar links */
    section[data-testid="stSidebar"] a {
        color: #ff8fab !important;
    }
    
    /* Sidebar navigation items */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:hover span {
        color: #ff8fab !important;
    }
    
    /* Active page highlight */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li[aria-selected="true"] {
        background: rgba(255, 107, 156, 0.2) !important;
        border-radius: 10px;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 30%, #ffc3d4 60%, #ff6b9d 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .hero-heart {
        font-size: 10rem;
        animation: heartbeat 1.2s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 0 40px rgba(255, 107, 156, 0.6));
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        15% { transform: scale(1.2); }
        30% { transform: scale(1); }
        45% { transform: scale(1.15); }
        60% { transform: scale(1); }
    }
    
    /* SECTION TITLES - BRIGHT WHITE */
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff !important;
        text-align: center;
        margin: 3rem 0 1rem 0;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #cccccc;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Stat Cards - Vibrant */
    .stat-card {
        background: linear-gradient(135deg, rgba(255, 107, 156, 0.25) 0%, rgba(138, 43, 226, 0.2) 100%);
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        border: 2px solid rgba(255, 107, 156, 0.5);
        transition: all 0.4s ease;
        margin: 0.5rem;
        box-shadow: 0 10px 40px rgba(255, 107, 156, 0.2);
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(255, 107, 156, 0.4);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: #ff8fab;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #ffffff;
        font-weight: 500;
    }
    
    /* Risk Factor Cards */
    .risk-card {
        background: linear-gradient(135deg, rgba(255, 87, 87, 0.2) 0%, rgba(255, 140, 66, 0.1) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.6rem 0;
        border-left: 4px solid #ff5757;
        transition: all 0.3s ease;
    }
    
    .risk-card:hover {
        transform: translateX(10px);
        background: linear-gradient(135deg, rgba(255, 87, 87, 0.3) 0%, rgba(255, 140, 66, 0.2) 100%);
    }
    
    .risk-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .risk-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    
    .risk-desc {
        font-size: 0.95rem;
        color: #cccccc;
        line-height: 1.5;
    }
    
    /* Prevention Cards */
    .prevention-card {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.15) 0%, rgba(0, 200, 150, 0.1) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.6rem 0;
        border-left: 4px solid #00ffaa;
        transition: all 0.3s ease;
    }
    
    .prevention-card:hover {
        transform: translateX(10px);
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.25) 0%, rgba(0, 200, 150, 0.15) 100%);
    }
    
    .prevention-card .risk-title {
        color: #00ffaa;
    }
    
    /* Warning banner */
    .warning-banner {
        background: rgba(255, 180, 0, 0.15);
        border: 1px solid rgba(255, 180, 0, 0.4);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .warning-text {
        color: #ffcc00;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* CTA Button */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(255, 107, 156, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 156, 0.5) !important;
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
    
    button[data-testid="stBaseButton-headerNoPadding"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    [data-testid="collapsedControl"] {
        color: #ffffff !important;
    }
    
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar Content
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 2rem; margin: 0;">🫀</p>
        <h2 style="color: #ff8fab; margin: 0.5rem 0;">HeartGuard</h2>
        <p style="color: #aaa; font-size: 0.85rem;">Heart Attack Prediction System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">📊 Quick Facts - India</p>
        <ul style="color: #e0e0e0; font-size: 0.9rem; line-height: 1.8;">
            <li>2.8M deaths/year from CVD</li>
            <li>28% of all deaths</li>
            <li>80% are preventable</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">🎓 Project Info</p>
        <p style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.6;">
        Final Year Major Project<br>
        <strong>Topic:</strong> Heart Attack Prediction using Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔬 Check Your Risk", use_container_width=True):
        st.switch_page("pages/1_🔬_Predict_Risk.py")

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-heart">🫀</div>
    <h1 class="hero-title">HeartGuard</h1>
    <p class="hero-subtitle">AI-Powered Heart Disease Risk Assessment & Awareness Platform</p>
</div>
""", unsafe_allow_html=True)

# Warning Banner
st.markdown("""
<div class="warning-banner">
    <p class="warning-text">⚠️ This tool is for educational purposes only. Always consult healthcare professionals for medical advice.</p>
</div>
""", unsafe_allow_html=True)

# Statistics Section - INDIA FOCUSED
st.markdown('<h2 class="section-title">📊 Heart Disease in India</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">India has one of the highest burdens of cardiovascular disease in the world</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">2.8M</div>
        <div class="stat-label">Deaths per year in India</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">28%</div>
        <div class="stat-label">Of all deaths in India</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">1 in 4</div>
        <div class="stat-label">Indians at risk by age 40</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">272M</div>
        <div class="stat-label">Indians with heart conditions</div>
    </div>
    """, unsafe_allow_html=True)

# Indian Context Section
st.markdown('<h2 class="section-title">🇮🇳 Why India Is At High Risk</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Unique factors contributing to heart disease in India</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">🧬</div>
        <div class="risk-title">Genetic Predisposition</div>
        <div class="risk-desc">South Asians have a higher genetic risk for heart disease, with heart attacks occurring 10 years earlier than in other populations</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">🍽️</div>
        <div class="risk-title">Dietary Habits</div>
        <div class="risk-desc">High consumption of refined carbs, trans fats, and low fiber intake contribute to rising cholesterol levels</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">🏙️</div>
        <div class="risk-title">Urbanization & Stress</div>
        <div class="risk-desc">Rapid urbanization has led to sedentary lifestyles and increased work-related stress</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">💉</div>
        <div class="risk-title">Diabetes Epidemic</div>
        <div class="risk-desc">India has 77+ million diabetics, making it the "Diabetes Capital of the World" - a major CVD risk factor</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">🚬</div>
        <div class="risk-title">Tobacco Use</div>
        <div class="risk-desc">Over 275 million Indians use tobacco, significantly increasing cardiovascular risk</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-card">
        <div class="risk-icon">🌫️</div>
        <div class="risk-title">Air Pollution</div>
        <div class="risk-desc">Poor air quality in major cities contributes to 25% of heart disease deaths in India</div>
    </div>
    """, unsafe_allow_html=True)

# Prevention Section
st.markdown('<h2 class="section-title">💚 Prevention Is Key</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Simple lifestyle changes can dramatically reduce your risk</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="prevention-card">
        <div class="risk-icon">🏃</div>
        <div class="risk-title">Stay Active</div>
        <div class="risk-desc">30 minutes of walking, yoga, or exercise daily can reduce risk by 30-40%</div>
    </div>
    <div class="prevention-card">
        <div class="risk-icon">🥗</div>
        <div class="risk-title">Eat Healthy</div>
        <div class="risk-desc">Include more vegetables, dal, whole grains; reduce oil, sugar, and processed foods</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="prevention-card">
        <div class="risk-icon">😴</div>
        <div class="risk-title">Quality Sleep</div>
        <div class="risk-desc">7-8 hours of sleep helps your heart recover and reduces stress hormones</div>
    </div>
    <div class="prevention-card">
        <div class="risk-icon">🧘</div>
        <div class="risk-title">Manage Stress</div>
        <div class="risk-desc">Practice yoga, meditation, or pranayama to control blood pressure naturally</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="prevention-card">
        <div class="risk-icon">🚭</div>
        <div class="risk-title">Quit Tobacco</div>
        <div class="risk-desc">Quit smoking, gutka, and pan masala - risk drops 50% within 1 year of quitting</div>
    </div>
    <div class="prevention-card">
        <div class="risk-icon">🩺</div>
        <div class="risk-title">Regular Checkups</div>
        <div class="risk-desc">Get BP, blood sugar, and lipid profile checked annually after age 30</div>
    </div>
    """, unsafe_allow_html=True)

# CTA Section
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h2 style="color: #ffffff; font-size: 2.2rem; margin-bottom: 0.8rem;">Ready to Check Your Heart Health?</h2>
    <p style="color: #aaaaaa; font-size: 1.1rem; margin-bottom: 1.5rem;">Our AI-powered tool analyzes clinical parameters to assess your risk</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔬 Check Your Risk Now", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🔬_Predict_Risk.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; color: #666;">
    <p style="font-size: 1rem;">🫀 HeartGuard - Heart Attack Prediction System</p>
    <p style="font-size: 0.8rem;">Final Year Major Project | Machine Learning in Healthcare | © 2024-2025</p>
</div>
""", unsafe_allow_html=True)
