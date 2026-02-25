# Smart Bus Arrival Time Prediction System - Test Cases
# Use these commands to test the API directly

## Test 1: Basic Prediction (Short Distance, Good Conditions)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 15.5, "traffic_level": "Low", "weather": "Sunny"}'
```

Expected Response:
```json
{
    "success": true,
    "predicted_arrival_time": 18.45,
    "unit": "minutes",
    "distance": 15.5,
    "traffic_level": "Low",
    "weather": "Sunny",
    "message": "Bus will arrive in approximately 18.45 minutes"
}
```

---

## Test 2: Medium Distance, Medium Conditions

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 35.0, "traffic_level": "Medium", "weather": "Cloudy"}'
```

Expected Response:
```json
{
    "success": true,
    "predicted_arrival_time": 42.30,
    "unit": "minutes",
    "distance": 35.0,
    "traffic_level": "Medium",
    "weather": "Cloudy",
    "message": "Bus will arrive in approximately 42.30 minutes"
}
```

---

## Test 3: Long Distance, Bad Conditions

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 55.0, "traffic_level": "High", "weather": "Rainy"}'
```

Expected Response:
```json
{
    "success": true,
    "predicted_arrival_time": 75.65,
    "unit": "minutes",
    "distance": 55.0,
    "traffic_level": "High",
    "weather": "Rainy",
    "message": "Bus will arrive in approximately 75.65 minutes"
}
```

---

## Test 4: Invalid Distance (Error Test)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 150, "traffic_level": "Low", "weather": "Sunny"}'
```

Expected Response (Status 400):
```json
{
    "error": "Invalid distance. Please enter distance between 0 and 100 km"
}
```

---

## Test 5: Invalid Traffic Level (Error Test)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 25, "traffic_level": "VeryHigh", "weather": "Sunny"}'
```

Expected Response (Status 400):
```json
{
    "error": "Invalid traffic level. Choose: Low, Medium, or High"
}
```

---

## Test 6: Invalid Weather (Error Test)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance": 25, "traffic_level": "Low", "weather": "Snowy"}'
```

Expected Response (Status 400):
```json
{
    "error": "Invalid weather. Choose: Sunny, Rainy, or Cloudy"
}
```

---

## Using Python Requests Library for Testing

```python
import requests
import json

API_URL = "http://localhost:5000/predict"

# Test 1: Normal prediction
test_data = {
    "distance": 30.5,
    "traffic_level": "Medium",
    "weather": "Cloudy"
}

response = requests.post(API_URL, json=test_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

---

## Using JavaScript Fetch (Browser Console)

```javascript
// Test in browser console while on http://localhost:5000

fetch('/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        distance: 25.5,
        traffic_level: 'Medium',
        weather: 'Sunny'
    })
})
.then(response => response.json())
.then(data => console.log('Result:', data))
.catch(error => console.error('Error:', error));
```

---

## Performance Benchmarks

| Distance | Traffic | Weather | Predicted Time | Time Unit |
|----------|---------|---------|-----------------|-----------|
| 10 km    | Low     | Sunny   | ~12-15 min      | minutes   |
| 25 km    | Medium  | Cloudy  | ~28-32 min      | minutes   |
| 40 km    | High    | Rainy   | ~55-65 min      | minutes   |
| 60 km    | High    | Rainy   | ~75-90 min      | minutes   |

Note: Exact values vary due to random average speed in model

---

## Model Performance Metrics

When you run `python train_model.py`, you should see:

```
Training Metrics:
  Mean Squared Error (MSE): ~45
  Root Mean Squared Error (RMSE): ~6.7 minutes
  Mean Absolute Error (MAE): ~4.9 minutes
  R² Score: ~0.88

Testing Metrics:
  Mean Squared Error (MSE): ~52
  Root Mean Squared Error (RMSE): ~7.2 minutes
  Mean Absolute Error (MAE): ~5.2 minutes
  R² Score: ~0.85
```

This means:
- Model explains ~85% of the variance
- Average prediction error: ±5-7 minutes
- Works well for practical bus time predictions

---

## Stress Testing

To test API under load:

```python
import requests
import time
import threading

def stress_test(num_requests=100):
    url = "http://localhost:5000/predict"
    
    def make_request():
        data = {
            "distance": 25,
            "traffic_level": "Medium",
            "weather": "Sunny"
        }
        try:
            response = requests.post(url, json=data, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    results = []
    for i in range(num_requests):
        results.append(make_request())
    
    success_rate = sum(results) / len(results) * 100
    print(f"Success Rate: {success_rate}%")
    print(f"Successful: {sum(results)}/{len(results)}")

# Run test
stress_test(100)
```

---

## Tips for Testing

1. **Always ensure Flask server is running**
   ```bash
   python app.py
   ```

2. **Open another terminal for testing** while server is running

3. **Use http://localhost:5000 (not https)** for local testing

4. **Check network connectivity** if connection is refused

5. **Verify JSON format** is valid before sending

6. **Enable debug output** in browser (F12 > Console) for web testing

---

## Integration Testing with Frontend

1. Open: http://localhost:5000
2. Fill in the form:
   - Distance: 30
   - Traffic Level: Medium
   - Weather: Sunny
3. Click "Predict Arrival Time"
4. Verify result displays correctly
5. Try different combinations

---
