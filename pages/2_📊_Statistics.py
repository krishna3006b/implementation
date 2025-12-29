import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Statistics - HeartGuard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Vibrant Theme
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
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff !important;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(255, 107, 156, 0.2) 0%, rgba(138, 43, 226, 0.15) 100%);
        border-radius: 24px;
        padding: 2rem;
        border: 2px solid rgba(255, 107, 156, 0.4);
        margin-bottom: 1rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 40px rgba(255, 107, 156, 0.2);
        text-align: center;
    }
    
    .stat-box:hover {
        transform: translateY(-10px);
        border-color: #ff8fab;
        box-shadow: 0 20px 60px rgba(255, 107, 156, 0.4);
    }
    
    .fact-card {
        background: linear-gradient(135deg, rgba(255, 107, 156, 0.2) 0%, rgba(255, 140, 66, 0.1) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 0.5rem 0;
        border-left: 5px solid #ff8fab;
        box-shadow: 0 8px 30px rgba(255, 107, 156, 0.2);
    }
    
    .fact-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ff8fab;
    }
    
    .fact-text {
        color: #ffffff;
        font-size: 1rem;
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
        box-shadow: 0 10px 30px rgba(255, 107, 156, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
    }
    
    /* Style the header to be dark */
    header[data-testid="stHeader"] {
        background: #0f0f1a !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Make sidebar toggle arrow white */
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

# Sidebar Content
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 2rem; margin: 0;">📊</p>
        <h2 style="color: #ff8fab; margin: 0.5rem 0;">Statistics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">📚 Data Sources</p>
        <ul style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.8;">
            <li>ICMR (Indian Council of Medical Research)</li>
            <li>Indian Heart Association</li>
            <li>WHO India</li>
            <li>Lancet Studies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #ffffff;">
        <p style="color: #ff8fab; font-weight: 600; margin-bottom: 0.5rem;">🇮🇳 Key Insight</p>
        <p style="color: #e0e0e0; font-size: 0.85rem; line-height: 1.6;">
        Indians experience heart attacks <strong>10 years earlier</strong> than the global average.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Dashboard.py")

# Page Header
st.markdown('<h1 class="page-title">📊 Heart Disease Statistics - India</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Understanding the cardiovascular disease burden in India</p>', unsafe_allow_html=True)

# India Statistics
st.markdown('<h2 class="section-title">🇮🇳 India Overview</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="fact-number">2.8M</div>
        <div class="fact-text">Deaths per year in India</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="fact-number">28%</div>
        <div class="fact-text">Of all deaths in India</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="fact-number">272M</div>
        <div class="fact-text">Indians with CVD conditions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="fact-number">54.5M</div>
        <div class="fact-text">Living with heart disease</div>
    </div>
    """, unsafe_allow_html=True)

# Age Distribution Chart - India
st.markdown("---")
st.markdown('<h2 class="section-title">📈 CVD Prevalence by Age in India</h2>', unsafe_allow_html=True)

age_data = pd.DataFrame({
    'Age Group': ['25-34', '35-44', '45-54', '55-64', '65-74', '75+'],
    'Prevalence %': [5, 12, 22, 38, 52, 65]
})

st.bar_chart(age_data.set_index('Age Group'), color='#ff6b9d')
st.caption("Prevalence of cardiovascular disease by age group in India (Source: ICMR)")

# State-wise Statistics
st.markdown("---")
st.markdown('<h2 class="section-title">🗺️ State-wise CVD Burden</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h4 style="color: #ff8fab;">Punjab</h4>
        <div class="fact-number">15.6%</div>
        <div class="fact-text">Highest CVD prevalence</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h4 style="color: #ff8fab;">Kerala</h4>
        <div class="fact-number">14.8%</div>
        <div class="fact-text">High urban CVD rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h4 style="color: #ff8fab;">Tamil Nadu</h4>
        <div class="fact-number">13.5%</div>
        <div class="fact-text">Rising CVD cases</div>
    </div>
    """, unsafe_allow_html=True)

# Gender comparison India
st.markdown("---")
st.markdown('<h2 class="section-title">👥 Gender Statistics - India</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="fact-card" style="border-color: #4a90d9;">
        <h3 style="color: #6bb3ff; font-size: 1.4rem;">👨 Men in India</h3>
        <div class="fact-number" style="color: #6bb3ff;">17.8%</div>
        <div class="fact-text">Of Indian men affected by CVD</div>
        <br>
        <p style="color: #c0c0c0; line-height: 1.8;">
        ✓ Average age of first heart attack: 50 years<br>
        ✓ 10 years earlier than global average<br>
        ✓ Higher risk due to stress & smoking
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="fact-card" style="border-color: #e84393;">
        <h3 style="color: #ff8fab; font-size: 1.4rem;">👩 Women in India</h3>
        <div class="fact-number" style="color: #ff8fab;">13.2%</div>
        <div class="fact-text">Of Indian women affected by CVD</div>
        <br>
        <p style="color: #c0c0c0; line-height: 1.8;">
        ✓ Risk increases sharply after menopause<br>
        ✓ Often underdiagnosed due to different symptoms<br>
        ✓ PCOS increases risk in younger women
        </p>
    </div>
    """, unsafe_allow_html=True)

# Risk Factors Chart - India
st.markdown("---")
st.markdown('<h2 class="section-title">⚠️ Major Risk Factors in India</h2>', unsafe_allow_html=True)

risk_data = pd.DataFrame({
    'Risk Factor': ['Hypertension', 'Diabetes', 'Tobacco Use', 'Obesity', 'Air Pollution', 'Physical Inactivity', 'Unhealthy Diet'],
    'Contribution %': [35, 28, 25, 20, 18, 15, 12]
})

st.bar_chart(risk_data.set_index('Risk Factor'), color='#ff6b9d', horizontal=True)
st.caption("Contribution of risk factors to CVD in India (Source: Indian Heart Association)")

# Comparison with Global
st.markdown("---")
st.markdown('<h2 class="section-title">🌍 India vs Global Comparison</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h4 style="color: #ff8fab;">🇮🇳 India</h4>
        <div class="fact-number">2.8M</div>
        <div class="fact-text">CVD deaths per year</div>
        <p style="color: #aaa; margin-top: 1rem;">Average age of first heart attack: <strong style="color: #ff8fab;">50 years</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h4 style="color: #ff8fab;">🌍 Global</h4>
        <div class="fact-number">17.9M</div>
        <div class="fact-text">CVD deaths per year</div>
        <p style="color: #aaa; margin-top: 1rem;">Average age of first heart attack: <strong style="color: #ff8fab;">60 years</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.markdown('<h2 class="section-title">💡 Key Takeaways for India</h2>', unsafe_allow_html=True)

st.success("""
**Important Facts for Indians:**
- ✅ Indians are at higher genetic risk - heart attacks occur 10 years earlier
- ✅ Up to **80%** of heart attacks are preventable with lifestyle changes
- ✅ Regular screening after age 30 is crucial
- ✅ Traditional practices like yoga can significantly reduce risk
""")

# CTA
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔬 Check Your Risk Now", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🔬_Predict_Risk.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>📊 Data sources: ICMR, Indian Heart Association, WHO India, Lancet</p>
    <p style="font-size: 0.8rem;">Final Year Major Project | Heart Attack Prediction using ML</p>
</div>
""", unsafe_allow_html=True)
