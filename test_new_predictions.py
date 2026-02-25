"""
Test Script for New Bus Arrival Prediction System (V2.0)
Demonstrates predictions using Bus Number and Destination as inputs
"""

import requests
import json

API_URL = "http://localhost:5000/predict"

def test_prediction(bus_number, destination, day, time_period, stop_seq):
    """Make a test prediction"""
    
    data = {
        "bus_number": bus_number,
        "destination": destination,
        "day_of_week": day,
        "time_period": time_period,
        "stop_sequence": stop_seq
    }
    
    print(f"\n{'='*60}")
    print(f"TEST: {bus_number} → {destination}")
    print(f"{'='*60}")
    print(f"Day: {day} | Time: {time_period} | Stop: #{stop_seq}")
    
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ PREDICTION SUCCESSFUL")
            print(f"  Predicted Arrival Time: {result['predicted_arrival_time']} minutes")
            print(f"  Message: {result['message']}")
        else:
            result = response.json()
            print(f"\n✗ ERROR: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"\n✗ CONNECTION ERROR: {str(e)}")

print("\n" + "="*60)
print("SMART BUS ARRIVAL PREDICTION SYSTEM - V2.0 TEST")
print("Bus Number & Destination Based Predictions")
print("="*60)

# Test Case 1: Morning commute to nearby location
test_prediction("BUS001", "Nagercoil", "Monday", "Morning", 1)

# Test Case 2: Afternoon trip to longer distance destination
test_prediction("BUS003", "Kanyakumari", "Tuesday", "Afternoon", 4)

# Test Case 3: Evening peak hours
test_prediction("BUS005", "Marthandam", "Wednesday", "Evening", 3)

# Test Case 4: Night ride
test_prediction("BUS002", "Colachel", "Thursday", "Night", 2)

# Test Case 5: Weekend travel
test_prediction("BUS007", "Thuckalay", "Saturday", "Morning", 5)

# Test Case 6: Far destination with multiple stops
test_prediction("BUS008", "Padmanabhapuram", "Friday", "Evening", 6)

# Test Case 7: Last stop
test_prediction("BUS004", "Suchindram", "Sunday", "Afternoon", 7)

# Test Case 8: Different bus, same destination
test_prediction("BUS006", "Kulasekaram", "Monday", "Morning", 3)

print("\n" + "="*60)
print("✓ ALL TESTS COMPLETED")
print("="*60)
print("\nFeatures Used:")
print("  • Bus Numbers: BUS001 to BUS008")
print("  • Destinations: 8 locations in Kanyakumari district")
print("  • Days: Monday to Sunday")
print("  • Time Periods: Morning, Afternoon, Evening, Night")
print("  • Stop Sequence: 1-7 (position in route)")
print("="*60)
