import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="PULSEPRO AI | Global Prosperity",
    page_icon="🌍",
    layout="wide"
)

# 2. ASSET LOADING (Model & Data)
@st.cache_resource
def load_assets():
    # Load Machine Learning Model
    model_path = os.path.join(os.path.dirname(__file__), 'prosperity_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Load CSV Data
    df = pd.read_csv('Cleaned_Prosperity_Data.csv')
    
    # AUTO-DETECT COUNTRY COLUMN (Fixes KeyError)
    possible_names = ['Country Name', 'Country', 'Nation', 'country', 'name']
    country_col = next((col for col in df.columns if col in possible_names), df.columns[0])
    
    return model, df, country_col

try:
    model, df, country_col = load_assets()
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# 3. PREMIUM CSS STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #020617;
    }
    
    .main-title {
        font-size: 3.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #3b82f6, #2dd4bf);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .prediction-container {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 24px; padding: 40px; text-align: center;
        margin-top: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .glow-metric {
        font-size: 5.5rem; font-weight: 800; color: #fff;
        text-shadow: 0 0 25px rgba(59, 130, 246, 0.6);
        margin: 10px 0;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 10px 10px 0 0; padding: 10px 20px; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER & SELECTION
st.markdown('<h1 class="main-title">PULSEPRO AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; font-size:1.2rem; margin-bottom:2rem;">Predicting National Prosperity through 12 Economic Pillars</p>', unsafe_allow_html=True)

# Country Dropdown
countries = sorted(df[country_col].unique().tolist())
selected_country = st.selectbox("🌐 Select a Country to Auto-Fill Pillars:", ["Manual Simulation"] + countries)

# Data Mapping Logic
if selected_country != "Manual Simulation":
    country_data = df[df[country_col] == selected_country].iloc[0]
    # We use .get() to avoid errors if a specific pillar name is slightly different
    vals = [float(country_data.get(col, 50.0)) for col in df.columns if col != country_col]
else:
    vals = [50.0] * 12

# 5. INTERACTIVE PILLARS (TABS)
tab1, tab2, tab3 = st.tabs(["🏛️ Rule of Law", "⚖️ Gov Size", "💰 Market Efficiency"])

with tab1:
    c1, c2 = st.columns(2)
    p1 = c1.slider("Property Rights", 0.0, 100.0, float(vals[0] if len(vals)>0 else 50))
    p2 = c2.slider("Judicial Effectiveness", 0.0, 100.0, float(vals[1] if len(vals)>1 else 50))
    p3 = c1.slider("Government Integrity", 0.0, 100.0, float(vals[2] if len(vals)>2 else 50))
    p4 = c2.slider("Tax Burden", 0.0, 100.0, float(vals[3] if len(vals)>3 else 50))

with tab2:
    c3, c4 = st.columns(2)
    p5 = c3.slider("Gov Spending", 0.0, 100.0, float(vals[4] if len(vals)>4 else 50))
    p6 = c4.slider("Fiscal Health", 0.0, 100.0, float(vals[5] if len(vals)>5 else 50))
    p7 = c3.slider("Business Freedom", 0.0, 100.0, float(vals[6] if len(vals)>6 else 50))
    p8 = c4.slider("Labor Freedom", 0.0, 100.0, float(vals[7] if len(vals)>7 else 50))

with tab3:
    c5, c6 = st.columns(2)
    p9 = c5.slider("Monetary Freedom", 0.0, 100.0, float(vals[8] if len(vals)>8 else 50))
    p10 = c6.slider("Trade Freedom", 0.0, 100.0, float(vals[9] if len(vals)>9 else 50))
    p11 = c5.slider("Investment Freedom", 0.0, 100.0, float(vals[10] if len(vals)>10 else 50))
    p12 = c6.slider("Financial Freedom", 0.0, 100.0, float(vals[11] if len(vals)>11 else 50))

# 6. AI SIMULATION LOGIC
st.markdown("---")
if st.button("🚀 INITIATE PROSPERITY SIMULATION", use_container_width=True):
    # Combine inputs into the exact 12-feature array
    input_features = np.array([[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]])
    
    # Calculate Prediction
    prediction = model.predict(input_features)[0]
    
    # Calculate Prosperity Score (Average of 12 pillars)
    overall_score = np.mean(input_features)

    st.markdown(f"""
        <div class="prediction-container">
            <p style="letter-spacing: 3px; color: #60a5fa; font-weight: 700; margin-bottom: 0;">PROSPERITY INDEX SCORE</p>
            <div class="glow-metric">{round(overall_score, 1)}%</div>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 12px; display: inline-block;">
                <span style="color: #94a3b8;">Predicted GDP Impact:</span> 
                <span style="color: #2dd4bf; font-weight: 800; font-size: 1.4rem;">{round(prediction, 2)}%</span>
            </div>
            <p style="color: #475569; margin-top: 20px; font-size: 0.8rem;">
                Simulation based on Random Forest Regression Analysis
            </p>
        </div>
    """, unsafe_allow_html=True)

# 7. FOOTER / SIDEBAR
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3859/3859125.png", width=100)
st.sidebar.title("Simulation Lab")
st.sidebar.write("This tool uses ML to show how policy changes in **Rule of Law**, **Gov Size**, and **Market Access** create national wealth.")
st.sidebar.markdown("---")
st.sidebar.caption("Santhosh | Technical Trainer | B.Tech 2026")
