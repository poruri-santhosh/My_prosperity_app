import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="PULSEPRO AI | Global Insights", page_icon="🌍", layout="wide")

# 2. LOAD DATA & MODEL
@st.cache_resource
def load_assets():
    # Load Model
    model_path = os.path.join(os.path.dirname(__file__), 'prosperity_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Load CSV for Country Data
    df = pd.read_csv('Cleaned_Prosperity_Data.csv')
    return model, df

model, df = load_assets()

# 3. PREMIUM CSS (Now with "Country Card" styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; background: #020617; }
    
    .main-title {
        font-size: 3rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #3b82f6, #2dd4bf);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .prediction-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 20px; padding: 40px; text-align: center;
        margin-top: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }
    
    .percentage-text {
        font-size: 5rem; font-weight: 800; color: #3b82f6;
        text-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER & COUNTRY SELECTOR
st.markdown('<h1 class="main-title">PULSEPRO AI SIMULATOR</h1>', unsafe_allow_html=True)

# Country Selection Logic
countries = df['Country Name'].unique().tolist()
selected_country = st.selectbox("🌐 Select a Country to Load Baseline Data:", ["Manual Entry"] + countries)

# Set defaults based on selection
if selected_country != "Manual Entry":
    row = df[df['Country Name'] == selected_country].iloc[0]
    # Map CSV columns to your slider variables
    d_prop, d_judic, d_gov_int, d_tax = row['Property Rights'], row['Judicial Effectiveness'], row['Government Integrity'], row['Tax Burden']
    d_gov_sp, d_fiscal, d_busin, d_labor = row['Gov Spending'], row['Fiscal Health'], row['Business Freedom'], row['Labor Freedom']
    d_monet, d_trade, d_invest, d_finan = row['Monetary Freedom'], row['Trade Freedom'], row['Investment Freedom'], row['Financial Freedom']
else:
    d_prop = d_judic = d_gov_int = d_tax = d_gov_sp = d_fiscal = d_busin = d_labor = d_monet = d_trade = d_invest = d_finan = 50.0

# 5. INPUT TABS
tab1, tab2, tab3 = st.tabs(["🏛️ Legal & Gov", "⚖️ Gov Size", "💰 Open Markets"])

with tab1:
    c1, c2 = st.columns(2)
    prop = c1.slider("Property Rights", 0.0, 100.0, float(d_prop))
    judic = c2.slider("Judicial Effectiveness", 0.0, 100.0, float(d_judic))
    gov_int = c1.slider("Gov Integrity", 0.0, 100.0, float(d_gov_int))
    tax = c2.slider("Tax Burden", 0.0, 100.0, float(d_tax))

with tab2:
    c3, c4 = st.columns(2)
    gov_sp = c3.slider("Gov Spending", 0.0, 100.0, float(d_gov_sp))
    fiscal = c4.slider("Fiscal Health", 0.0, 100.0, float(d_fiscal))
    busin = c3.slider("Business Freedom", 0.0, 100.0, float(d_busin))
    labor = c4.slider("Labor Freedom", 0.0, 100.0, float(d_labor))

with tab3:
    c5, c6 = st.columns(2)
    monet = c5.slider("Monetary Freedom", 0.0, 100.0, float(d_monet))
    trade = c6.slider("Trade Freedom", 0.0, 100.0, float(d_trade))
    invest = c5.slider("Investment Freedom", 0.0, 100.0, float(d_invest))
    finan = c6.slider("Financial Freedom", 0.0, 100.0, float(d_finan))

# 6. SIMULATION & PERCENTAGE CALCULATION
st.markdown("---")
if st.button("🚀 EXECUTE AI PROSPERITY ANALYSIS", use_container_width=True):
    # Predict
    features = np.array([[prop, judic, gov_int, tax, gov_sp, fiscal, busin, labor, monet, trade, invest, finan]])
    prediction = model.predict(features)[0]
    
    # Logic: If your model predicts GDP growth (e.g. 5%), let's show it. 
    # If you want a "Prosperity Score" out of 100, we can calculate (Avg of Pillars)
    prosperity_score = np.mean(features)

    st.markdown(f"""
        <div class="prediction-container">
            <p style="color: #94a3b8; font-weight: 700; letter-spacing: 2px;">GLOBAL PROSPERITY INDEX</p>
            <div class="percentage-text">{round(prosperity_score, 1)}%</div>
            <p style="color: #60a5fa; font-size: 1.2rem;">Predicted GDP Impact: <b>{round(prediction, 2)}%</b></p>
            <p style="color: #475569; font-size: 0.9rem; margin-top: 15px;">
                Analysis for <b>{selected_country if selected_country != "Manual Entry" else "Custom Model"}</b> complete.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.title("PULSEPRO AI")
st.sidebar.info("This AI simulates how changes in Law, Tax, and Trade impact a nation's wealth.")
