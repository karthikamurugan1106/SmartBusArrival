"""
Test script for Smart Bus Arrival Time Prediction System
Tests the API with multiple scenarios
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000'

def test_prediction(test_name, data):
    """Test a prediction and display results"""
    print('\n' + '=' * 70)
    print(f'{test_name}')
    print('=' * 70)
    print(f'Input: {json.dumps(data, indent=2)}')
    try:
        response = requests.post(f'{BASE_URL}/predict', json=data, timeout=5)
        result = response.json()
        print(f'Status Code: {response.status_code}')
        print(f'Response:\n{json.dumps(result, indent=2)}')
        return True
    except requests.exceptions.ConnectionError:
        print('Error: Cannot connect to Flask server. Make sure it\'s running on localhost:5000')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False

def main():
    """Run all tests"""
    print('\n' + '=' * 70)
    print('SMART BUS ARRIVAL TIME PREDICTION SYSTEM - API TEST SUITE')
    print('=' * 70)
    
    # Test Case 1: Short distance, good conditions
    test_prediction(
        'TEST 1: Short Distance, Good Conditions',
        {'distance': 15.5, 'traffic_level': 'Low', 'weather': 'Sunny'}
    )
    
    # Test Case 2: Medium distance, medium conditions
    test_prediction(
        'TEST 2: Medium Distance, Medium Conditions',
        {'distance': 35.0, 'traffic_level': 'Medium', 'weather': 'Cloudy'}
    )
    
    # Test Case 3: Long distance, bad conditions
    test_prediction(
        'TEST 3: Long Distance, Bad Conditions',
        {'distance': 55.0, 'traffic_level': 'High', 'weather': 'Rainy'}
    )
    
    # Test Case 4: Very short distance
    test_prediction(
        'TEST 4: Very Short Distance',
        {'distance': 8.5, 'traffic_level': 'Low', 'weather': 'Sunny'}
    )
    
    # Test Case 5: Maximum distance
    test_prediction(
        'TEST 5: Maximum Distance',
        {'distance': 95.0, 'traffic_level': 'High', 'weather': 'Rainy'}
    )
    
    # Test Case 6: Error handling - Invalid distance (too high)
    test_prediction(
        'TEST 6: Error Handling - Invalid Distance (>100 km)',
        {'distance': 150, 'traffic_level': 'Low', 'weather': 'Sunny'}
    )
    
    # Test Case 7: Error handling - Invalid traffic level
    test_prediction(
        'TEST 7: Error Handling - Invalid Traffic Level',
        {'distance': 30, 'traffic_level': 'VeryHigh', 'weather': 'Sunny'}
    )
    
    # Test Case 8: Error handling - Invalid weather
    test_prediction(
        'TEST 8: Error Handling - Invalid Weather',
        {'distance': 30, 'traffic_level': 'Medium', 'weather': 'Snowy'}
    )
    
    print('\n' + '=' * 70)
    print('✅ ALL TESTS COMPLETED!')
    print('=' * 70)

if __name__ == '__main__':
    main()
