import streamlit as st
import pickle
import numpy as np
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="PULSEPRO | Prosperity Predictor",
    page_icon="📈",
    layout="wide"
)

# 2. CUSTOM CSS (The "Beauty" Layer)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at center, #0f172a, #020617);
        color: #f1f5f9;
    }
    
    /* Card Styling */
    .prediction-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Header Styling */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Custom Slider Color */
    .stSlider > div [data-baseweb="slider"] {
        background-color: #1e293b;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOAD THE MODEL
@st.cache_resource # This makes the app super fast
def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'prosperity_model.pkl')
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# 4. SIDEBAR 
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3163/3163195.png", width=80)
    st.title("Settings")
    st.info("Adjust the scores (0-100) to see how economic policy impacts prosperity.")
    st.markdown("---")
    st.write("**Author:** Santhosh (ML Engineer)")

# 5. MAIN INTERFACE
st.title("PULSEPRO | Predictor Dashboard")
st.write("Simulate global economic outcomes using 12 pillars of freedom.")

# Organize Sliders into 3 categories
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏛️ Institutional")
    prop = st.slider("Property Rights", 0, 100, 50)
    judic = st.slider("Judicial Effectiveness", 0, 100, 50)
    gov_int = st.slider("Gov Integrity", 0, 100, 50)
    tax = st.slider("Tax Burden", 0, 100, 50)

with col2:
    st.subheader("⚖️ Government")
    gov_sp = st.slider("Gov Spending", 0, 100, 50)
    fiscal = st.slider("Fiscal Health", 0, 100, 50)
    busin = st.slider("Business Freedom", 0, 100, 50)
    labor = st.slider("Labor Freedom", 0, 100, 50)

with col3:
    st.subheader("💰 Market")
    monet = st.slider("Monetary Freedom", 0, 100, 50)
    trade = st.slider("Trade Freedom", 0, 100, 50)
    invest = st.slider("Investment Freedom", 0, 100, 50)
    finan = st.slider("Financial Freedom", 0, 100, 50)

# 6. PREDICTION LOGIC
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 RUN PROSPERITY SIMULATION", use_container_width=True):
    if model:
        # Array must be 2D: [[val1, val2...]]
        # CHECK ORDER: Make sure this matches your CSV columns!
        input_data = np.array([[
            prop, judic, gov_int, tax, gov_sp, fiscal, 
            busin, labor, monet, trade, invest, finan
        ]])
        
        prediction = model.predict(input_data)[0]
        
        # Display the result in a beautiful card
        st.markdown(f"""
            <div class="prediction-card">
                <p style="color: #94a3b8; font-weight: 600; margin-bottom: 5px;">PREDICTED ECONOMIC GROWTH</p>
                <h1 style="font-size: 4rem; margin: 0;">{round(prediction, 2)}%</h1>
                <p style="color: #3b82f6; margin-top: 10px;">Simulation Complete</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Model not available. Please verify 'prosperity_model.pkl' exists.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Developed for B.Tech Final Year Project | Data Analytics & ML")
