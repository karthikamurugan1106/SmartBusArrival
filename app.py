"""
Smart Bus Arrival Time Prediction System - Flask Backend
API endpoint for predicting bus arrival times
"""

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model, encoders, and scaler
MODEL_PATH = 'models/bus_model.joblib'
ENCODERS_PATH = 'models/encoders.joblib'
SCALER_PATH = 'models/scaler.joblib'

# Check if model exists
if not os.path.exists(MODEL_PATH):
    print("Error: Model not found! Please run 'python train_model.py' first.")
    exit(1)

# Load model, encoders, and scaler
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODERS_PATH)
scaler = joblib.load(SCALER_PATH)

print("✓ Model loaded successfully!")
print("✓ Encoders loaded successfully!")
print("✓ Scaler loaded successfully!")
print("✓ Flask server starting...")

@app.route('/')
def index():
    """
    Render the main HTML page
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint for predicting bus arrival time
    
    Expected JSON input:
    {
        "bus_number": "BUS001",
        "destination": "Kanyakumari",
        "day_of_week": "Monday",
        "time_period": 14,
        "stop_sequence": 3
    }
    
    Returns JSON with predicted arrival time
    """
    
    try:
        # Get data from request
        data = request.get_json()
        
        # Extract features
        bus_number = data.get('bus_number')
        destination = data.get('destination')
        day_of_week = data.get('day_of_week', 'Monday')
        time_period = data.get('time_period')  # Now numeric hour (0-23)
        stop_sequence = int(data.get('stop_sequence', 1))
        
        # Valid values
        valid_buses = ["BUS001", "BUS002", "BUS003", "BUS004", "BUS005", "BUS006", "BUS007", "BUS008"]
        valid_destinations = ["Nagercoil", "Kanyakumari", "Marthandam", "Colachel", "Thuckalay", "Kulasekaram", "Padmanabhapuram", "Suchindram"]
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Validate inputs
        if not bus_number or bus_number not in valid_buses:
            return jsonify({
                'error': f'Invalid bus number. Valid buses: {", ".join(valid_buses)}'
            }), 400
        
        if not destination or destination not in valid_destinations:
            return jsonify({
                'error': f'Invalid destination. Valid destinations: {", ".join(valid_destinations)}'
            }), 400
        
        if day_of_week not in valid_days:
            return jsonify({
                'error': f'Invalid day. Valid days: {", ".join(valid_days)}'
            }), 400
        
        # Validate time period (must be numeric hour 0-23)
        if time_period is None or not isinstance(time_period, int) or time_period < 0 or time_period > 23:
            return jsonify({
                'error': 'Invalid time period. Time must be hour (0-23)'
            }), 400
        
        if stop_sequence < 1 or stop_sequence > 7:
            return jsonify({
                'error': 'Invalid stop sequence. Enter between 1 and 7'
            }), 400
        
        # Encode categorical variables
        bus_encoded = encoders['bus_encoder'].transform([bus_number])[0]
        destination_encoded = encoders['destination_encoder'].transform([destination])[0]
        day_encoded = encoders['day_encoder'].transform([day_of_week])[0]
        # time_period is already numeric (0-23), no encoding needed
        
        # Create feature array for prediction
        # Features order: Bus_Number, Destination, Day_Of_Week, Time_Period, Stop_Sequence
        features = np.array([[
            bus_encoded,
            destination_encoded,
            day_encoded,
            time_period,
            stop_sequence
        ]])
        
        # Scale features using the trained scaler
        features_scaled = scaler.transform(features)
        
        # Make prediction
        predicted_time = model.predict(features_scaled)[0]
        
        # Round to 2 decimal places
        predicted_time = round(predicted_time, 2)
        
        # Build response
        response = {
            'success': True,
            'predicted_arrival_time': predicted_time,
            'unit': 'minutes',
            'bus_number': bus_number,
            'destination': destination,
            'day_of_week': day_of_week,
            'time_period': time_period,
            'stop_sequence': stop_sequence,
            'message': f'Bus {bus_number} will arrive in approximately {predicted_time} minutes'
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

@app.route('/api/info', methods=['GET'])
def info():
    """
    API endpoint to get model information
    """
    return jsonify({
        'system': 'Smart Bus Arrival Time Prediction System',
        'location': 'Kanyakumari District, Tamil Nadu',
        'model': 'Linear Regression',
        'version': '1.0.0'
    }), 200

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)