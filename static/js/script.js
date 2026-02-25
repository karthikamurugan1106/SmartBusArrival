/**
 * Smart Bus Arrival Time Prediction System - Frontend JavaScript
 * Handles form submission and API communication
 */

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const busNumberSelect = document.getElementById('busNumber');
const destinationSelect = document.getElementById('destination');
const dayOfWeekSelect = document.getElementById('dayOfWeek');
const timePeriodInput = document.getElementById('timePeriod');  // Now a time input
const stopSequenceSelect = document.getElementById('stopSequence');
const loadingDiv = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const resultCard = document.getElementById('resultCard');
const emptyState = document.getElementById('emptyState');

// Result elements
const arrivalTimeValue = document.getElementById('arrivalTimeValue');
const resultBus = document.getElementById('resultBus');
const resultDestination = document.getElementById('resultDestination');
const resultDay = document.getElementById('resultDay');
const resultTime = document.getElementById('resultTime');
const resultStop = document.getElementById('resultStop');
const predictionMessage = document.getElementById('predictionMessage');

/**
 * Event listener for form submission
 */
predictionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await makePrediction();
});

/**
 * Make prediction by calling Flask API
 */
async function makePrediction() {
    try {
        // Get form values
        const busNumber = busNumberSelect.value;
        const destination = destinationSelect.value;
        const dayOfWeek = dayOfWeekSelect.value;
        const timeInput = timePeriodInput.value;  // Get time in HH:MM format
        const stopSequence = parseInt(stopSequenceSelect.value);

        // Validate inputs
        if (!busNumber || !destination || !dayOfWeek || !timeInput || !stopSequence) {
            showError('Please fill in all fields');
            return;
        }

        // Extract hour and minute from time input (HH:MM format)
        const [hourStr, minuteStr] = timeInput.split(':');
        const hour = parseInt(hourStr);
        const minute = parseInt(minuteStr);
        const timePeriod = hour;

        // Check if time is between 11:30 PM to 3:30 AM (no/limited buses)
        const isMidnightHours = (hour === 23 && minute >= 30) || hour < 4;
        
        if (isMidnightHours) {
            showLoading(false);
            displayNoServiceMessage(busNumber, destination, dayOfWeek, timeInput, stopSequence);
            return;
        }

        // Show loading indicator
        showLoading(true);
        hideError();

        // Prepare request data
        const requestData = {
            bus_number: busNumber,
            destination: destination,
            day_of_week: dayOfWeek,
            time_period: timePeriod,
            stop_sequence: stopSequence
        };

        console.log('Sending prediction request:', requestData);

        // Make API call
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        // Hide loading indicator
        showLoading(false);

        // Check response status
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Prediction failed');
        }

        // Parse response
        const result = await response.json();

        console.log('Prediction result:', result);

        // Display results
        displayResults(result, busNumber, destination, dayOfWeek, timeInput, stopSequence);

    } catch (error) {
        console.error('Error:', error);
        showLoading(false);
        showError(`Error: ${error.message}`);
    }
}

/**
 * Display prediction results on the UI
 */
function displayResults(result, busNumber, destination, dayOfWeek, timePeriod, stopSequence) {
    if (!result.success) {
        showError(result.error);
        return;
    }

    // Update result values
    arrivalTimeValue.textContent = result.predicted_arrival_time.toFixed(2);
    resultBus.textContent = busNumber;
    resultDestination.textContent = destination;
    resultDay.textContent = dayOfWeek;
    resultTime.textContent = timePeriod;
    resultStop.textContent = stopSequence;
    predictionMessage.textContent = result.message;

    // Reset styling to normal (white background)
    resultCard.style.backgroundColor = '#ffffff';
    resultCard.style.borderLeft = '5px solid #28a745';  // Green border for success

    // Show result card and hide empty state
    resultCard.style.display = 'block';
    emptyState.style.display = 'none';

    // Scroll to results
    setTimeout(() => {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Show loading indicator
 */
function showLoading(isLoading) {
    if (isLoading) {
        loadingDiv.style.display = 'block';
    } else {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Display no service message for midnight hours (11:30 PM - 3:30 AM)
 */
function displayNoServiceMessage(busNumber, destination, dayOfWeek, timeInput, stopSequence) {
    // Update result card with no service message
    arrivalTimeValue.textContent = 'N/A';
    resultBus.textContent = busNumber;
    resultDestination.textContent = destination;
    resultDay.textContent = dayOfWeek;
    resultTime.textContent = timeInput;
    resultStop.textContent = stopSequence;
    predictionMessage.textContent = '⚠️ No Bus Service Available During Midnight Hours (11:30 PM - 3:30 AM).The Bus Sevice will be available after 3.30 AM. PLEASE COME BACK LATER!';

    // Show result card with styling
    resultCard.style.display = 'block';
    resultCard.style.backgroundColor = '#fff3cd';  // Light yellow warning color
    resultCard.style.borderLeft = '5px solid #ff6b6b';  // Red border for alert
    
    emptyState.style.display = 'none';

    // Scroll to results
    setTimeout(() => {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Clear results and show empty state
 */
function clearResults() {
    // Clear form
    predictionForm.reset();

    // Hide results
    resultCard.style.display = 'none';
    emptyState.style.display = 'block';

    // Clear error
    hideError();

    // Focus on form
    distanceInput.focus();

    // Scroll to form
    predictionForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Initialize page
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Smart Bus Arrival Time Prediction System - Loaded');
    
    // Set initial state
    emptyState.style.display = 'block';
    resultCard.style.display = 'none';
    loadingDiv.style.display = 'none';
    
    // Focus on first input
    distanceInput.focus();
});

/**
 * Input validation - remove as it's not needed for selects
 */
// All inputs are now dropdowns/selects, so validation is built-in

