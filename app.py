from flask import Flask, render_template, jsonify, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# 1. LOAD YOUR MODEL AT STARTUP
# This is faster and uses the model you already built
try:
    with open('prosperity_model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- Page Routes ---
@app.route('/')
def index():
    # Flask looks for this in the 'templates' folder
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

# --- ML API Route ---
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # 1. Get input from the web form
        data = request.json
        
        # 2. Convert dictionary to the correct array format for ML
        # Use the same features you used in your Notebook!
        input_data = np.array([list(data.values())])
        
        # 3. Predict using the LOADED model
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            "status": "success",
            "prediction": round(prediction, 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Running on port 5000
    app.run(debug=True, port=5000)