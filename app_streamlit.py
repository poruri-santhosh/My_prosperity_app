import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="PULSEPRO AI", page_icon="🌍", layout="wide")

# 2. LOAD ASSETS
@st.cache_resource
def load_assets():
    model_path = os.path.join(os.path.dirname(__file__), 'prosperity_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    df = pd.read_csv('Cleaned_Prosperity_Data.csv')
    
    # Detect Country Column
    possible_names = ['Country Name', 'Country', 'Nation', 'country', 'name']
    country_col = next((col for col in df.columns if col in possible_names), df.columns[0])
    
    return model, df, country_col

model, df, country_col = load_assets()

# 3. ADVANCED CSS (White text for selectors and cleaner dark mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #020617;
        color: white;
    }

    /* Make Country Selector and Labels White */
    label, .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .main-title {
        font-size: 3.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #3b82f6, #2dd4bf);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .prediction-container {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 24px; padding: 40px; text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }
    
    .glow-metric {
        font-size: 5rem; font-weight: 800; color: #fff;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER
st.markdown('<h1 class="main-title">PULSEPRO AI SIMULATOR</h1>', unsafe_allow_html=True)

# 5. DATA LOGIC (The Fix for the ValueError)
countries = sorted(df[country_col].unique().tolist())
selected_country = st.selectbox("🌐 Select a Nation to Analyze:", ["Manual Simulation"] + countries)

# Filter for numeric columns only (this prevents the ValueError)
numeric_df = df.select_dtypes(include=[np.number])
pillar_names = numeric_df.columns.tolist()

if selected_country != "Manual Simulation":
    country_row = df[df[country_col] == selected_country].iloc[0]
    # Get only numeric values for that country
    vals = [float(country_row[col]) for col in pillar_names]
else:
    vals = [50.0] * len(pillar_names)

# 6. SLIDER TABS
tab1, tab2, tab3 = st.tabs(["🏛️ Rule of Law", "⚖️ Gov Size", "💰 Open Markets"])

# Helper to safely get value from the vals list
def get_val(index):
    return vals[index] if index < len(vals) else 50.0

with tab1:
    c1, c2 = st.columns(2)
    p1 = c1.slider("Property Rights", 0.0, 100.0, get_val(0))
    p2 = c2.slider("Judicial Effectiveness", 0.0, 100.0, get_val(1))
    p3 = c1.slider("Government Integrity", 0.0, 100.0, get_val(2))
    p4 = c2.slider("Tax Burden", 0.0, 100.0, get_val(3))

with tab2:
    c3, c4 = st.columns(2)
    p5 = c3.slider("Gov Spending", 0.0, 100.0, get_val(4))
    p6 = c4.slider("Fiscal Health", 0.0, 100.0, get_val(5))
    p7 = c3.slider("Business Freedom", 0.0, 100.0, get_val(6))
    p8 = c4.slider("Labor Freedom", 0.0, 100.0, get_val(7))

with tab3:
    c5, c6 = st.columns(2)
    p9 = c5.slider("Monetary Freedom", 0.0, 100.0, get_val(8))
    p10 = c6.slider("Trade Freedom", 0.0, 100.0, get_val(9))
    p11 = c5.slider("Investment Freedom", 0.0, 100.0, get_val(10))
    p12 = c6.slider("Financial Freedom", 0.0, 100.0, get_val(11))

# 7. PREDICTION
st.markdown("---")
if st.button("🚀 EXECUTE AI ANALYSIS", use_container_width=True):
    # Prepare exactly 12 features for the model
    input_features = np.array([[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]])
    prediction = model.predict(input_features)[0]
    prosperity_score = np.mean(input_features)

    st.markdown(f"""
        <div class="prediction-container">
            <p style="letter-spacing: 2px; color: #60a5fa; font-weight: 700;">PROSPERITY INDEX</p>
            <div class="glow-metric">{round(prosperity_score, 1)}%</div>
            <div style="background: rgba(59, 130, 246, 0.15); padding: 10px 25px; border-radius: 50px; display: inline-block;">
                <span style="color: #94a3b8;">Predicted GDP Growth:</span> 
                <span style="color: #2dd4bf; font-weight: 800;">{round(prediction, 2)}%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
