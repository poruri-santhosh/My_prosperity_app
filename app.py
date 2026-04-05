from flask import Flask, render_template, jsonify, request
import pandas as pd
import pickle
import numpy as np
import os

app = Flask(__name__)

# 1. LOAD THE MODEL
# We use 'rb' (read binary) to load the saved pickle file
model = None
try:
    model_path = os.path.join(os.path.dirname(__file__), 'prosperity_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# --- Page Routes ---

@app.route('/')
def index():
    """Main Landing Page with Tableau Stories"""
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    """Deep Dive Analytics Page"""
    return render_template('analytics.html')

@app.route('/methodology')
def methodology():
    """Technical Details Page"""
    return render_template('methodology.html')

# --- ML API Route ---

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint that receives JSON data from the frontend,
    runs it through the ML model, and returns a prediction.
    """
    if model is None:
        return jsonify({"status": "error", "message": "Model not initialized on server"})

    try:
        # Get input data from the JavaScript 'fetch' request
        data = request.json
        
        # Convert dictionary values to a list, then to a 2D numpy array
        # IMPORTANT: The order of keys in your JS must match the training features
        features = np.array([list(data.values())])
        
        # Generate prediction
        prediction = model.predict(features)[0]
        
        return jsonify({
            "status": "success",
            "prediction": round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# --- Health Check (For Render Deployment) ---
@app.route('/status')
def status():
    return jsonify({"status": "online", "model_loaded": model is not None})

if __name__ == '__main__':
    # Local development settings
    app.run(debug=True, port=5000)