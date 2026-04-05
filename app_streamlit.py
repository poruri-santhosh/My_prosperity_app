import streamlit as st
import pickle
import numpy as np
import os

# Page Config
st.set_page_config(page_title="Prosperity Predictor", page_icon="📈", layout="centered")

# Custom CSS for the "PulsePro" look
st.markdown("""
    <style>
    .main { background-color: #020617; color: white; }
    .stSlider { color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("PULSEPRO | Prosperity Predictor")
st.write("Adjust the economic pillars below to predict a country's GDP Growth.")

# 1. Load the Model
model = None
try:
    with open('prosperity_model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"Model File Error: {e}")

# 2. User Inputs (The Dashboard Sliders)
st.subheader("Economic Freedom Pillars")
col1, col2 = st.columns(2)

with col1:
    trade = st.slider("Trade Freedom", 0.0, 100.0, 50.0)
    business = st.slider("Business Freedom", 0.0, 100.0, 50.0)
    investment = st.slider("Investment Freedom", 0.0, 100.0, 50.0)

with col2:
    monetary = st.slider("Monetary Freedom", 0.0, 100.0, 50.0)
    financial = st.slider("Financial Freedom", 0.0, 100.0, 50.0)
    property_r = st.slider("Property Rights", 0.0, 100.0, 50.0)

# 3. Prediction Logic
if st.button("Calculate Predicted Prosperity"):
    if model:
        # Note: Ensure the order of features matches your training data!
        # This example uses 6 features based on the sliders above
        input_data = np.array([[trade, business, investment, monetary, financial, property_r]])
        
        prediction = model.predict(input_data)[0]
        
        st.markdown("---")
        st.metric(label="Predicted GDP Growth", value=f"{round(prediction, 2)}%")
        st.info("This prediction is based on the 2022 Economic Freedom Index Model.")
    else:
        st.warning("Model not found. Please check your .pkl file.")
