"""
Smart Bus Arrival Time Prediction System - Model Training
Generates synthetic dataset for Tamil Nadu (Kanyakumari District)
and trains a Linear Regression model based on Bus Number and Destination
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define bus numbers in Kanyakumari district
BUS_NUMBERS = ["BUS001", "BUS002", "BUS003", "BUS004", "BUS005", "BUS006", "BUS007", "BUS008"]

# Define destination places in Kanyakumari district
DESTINATIONS = [
    "Nagercoil",
    "Kanyakumari",
    "Marthandam",
    "Colachel",
    "Thuckalay",
    "Kulasekaram",
    "Padmanabhapuram",
    "Suchindram"
]

# Days of week for realistic patterns
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def generate_dataset(num_records=250):
    """
    Generate synthetic dataset for bus arrival time prediction
    
    Parameters:
    num_records (int): Number of records to generate
    
    Returns:
    pd.DataFrame: Generated dataset
    """
    
    print(f"Generating synthetic dataset with {num_records} records...")
    
    data = {
        'Bus_Number': np.random.choice(BUS_NUMBERS, num_records),
        'Destination': np.random.choice(DESTINATIONS, num_records),
        'Day_Of_Week': np.random.choice(DAYS_OF_WEEK, num_records),
        'Time_Period': np.random.randint(0, 24, num_records),  # Hour (0-23)
        'Stop_Sequence': np.random.randint(1, 8, num_records),  # Sequence of stops (1-7)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate arrival time based on bus number, destination, and other factors
    arrival_times = []
    
    for idx, row in df.iterrows():
        # Base time for each destination (reduced for frequent bus scenario - 0-20 min range)
        destination_base_time = {
            "Nagercoil": 2,
            "Kanyakumari": 8,
            "Marthandam": 5,
            "Colachel": 10,
            "Thuckalay": 12,
            "Kulasekaram": 6,
            "Padmanabhapuram": 3,
            "Suchindram": 7
        }
        
        base_time = destination_base_time.get(row['Destination'], 6)
        
        # Add small variance based on stop sequence (later stops take slightly more time)
        stop_delay = row['Stop_Sequence'] * 0.5
        
        # Add time period factor (busy times = longer waits)
        # Time_Period is now hour (0-23)
        hour = row['Time_Period']
        if 6 <= hour < 12:  # Morning rush (6 AM - 12 PM)
            time_delay = 1.5
        elif 12 <= hour < 18:  # Afternoon (12 PM - 6 PM)
            time_delay = 0.5
        elif 18 <= hour < 21:  # Evening rush (6 PM - 9 PM)
            time_delay = 2
        else:  # Night and early morning
            time_delay = 1
        
        # Add day factor (weekends might be different)
        day_factor = 1 if row['Day_Of_Week'] in ["Saturday", "Sunday"] else 0.5
        
        # Bus number specific delays (some buses are slower)
        bus_delays = {"BUS001": 0.5, "BUS002": 1, "BUS003": 0, "BUS004": 0.8, 
                      "BUS005": 0.3, "BUS006": 1.2, "BUS007": 0.2, "BUS008": 0.7}
        bus_delay = bus_delays.get(row['Bus_Number'], 0.5)
        
        # Add random noise (small variance)
        noise = np.random.normal(0, 0.5)
        
        total_arrival_time = base_time + stop_delay + time_delay + day_factor + bus_delay + noise
        arrival_times.append(np.clip(total_arrival_time, 1, 20))  # Ensure within 1-20 minutes
    
    df['Arrival_Time_minutes'] = np.array(arrival_times).round(2)
    
    print(f"Dataset generated successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nDataset Statistics:")
    print(df.describe())
    
    return df


def preprocess_data(df):
    """
    Preprocess dataset - encode categorical variables
    
    Parameters:
    df (pd.DataFrame): Raw dataset
    
    Returns:
    tuple: (X features, y target, encoders for reverse transformation)
    """
    
    print("\nPreprocessing data...")
    
    # Create a copy to avoid modifying original
    df_processed = df.copy()
    
    # Separate features and target
    X = df_processed.drop('Arrival_Time_minutes', axis=1)
    y = df_processed['Arrival_Time_minutes']
    
    # Encode categorical variables
    # Store encoders for later use in predictions
    encoders = {}
    
    # Encode Bus Number
    le_bus = LabelEncoder()
    X.loc[:, 'Bus_Number'] = le_bus.fit_transform(X['Bus_Number'])
    encoders['bus_encoder'] = le_bus
    
    # Encode Destination
    le_destination = LabelEncoder()
    X.loc[:, 'Destination'] = le_destination.fit_transform(X['Destination'])
    encoders['destination_encoder'] = le_destination
    
    # Encode Day Of Week
    le_day = LabelEncoder()
    X.loc[:, 'Day_Of_Week'] = le_day.fit_transform(X['Day_Of_Week'])
    encoders['day_encoder'] = le_day
    
    # Time_Period is already numeric (hour 0-23), no encoding needed
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Encoded features:\n{X.head()}")
    
    return X, y, encoders


def train_model(X, y):
    """
    Train Linear Regression model
    
    Parameters:
    X (pd.DataFrame): Features
    y (pd.Series): Target variable
    
    Returns:
    tuple: (trained model, train metrics, test metrics)
    """
    
    print("\nSplitting data into training and testing sets...")
    
    # Split data into train and test (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # Scale features to improve model performance
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Ridge Regression model (better for this scenario)
    print("Training Ridge Regression model...")
    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train)
    
    # Make predictions on training and testing data
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(train_mse)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    # Print metrics
    print("\n" + "="*50)
    print("MODEL TRAINING RESULTS")
    print("="*50)
    print("\nTraining Metrics:")
    print(f"  Mean Squared Error (MSE): {train_mse:.4f}")
    print(f"  Root Mean Squared Error (RMSE): {train_rmse:.4f} minutes")
    print(f"  Mean Absolute Error (MAE): {train_mae:.4f} minutes")
    print(f"  R² Score: {train_r2:.4f}")
    
    print("\nTesting Metrics:")
    print(f"  Mean Squared Error (MSE): {test_mse:.4f}")
    print(f"  Root Mean Squared Error (RMSE): {test_rmse:.4f} minutes")
    print(f"  Mean Absolute Error (MAE): {test_mae:.4f} minutes")
    print(f"  R² Score: {test_r2:.4f}")
    
    print("\nModel Coefficients (Feature Importance):")
    feature_names = X.columns
    for name, coef in zip(feature_names, model.coef_):
        print(f"  {name}: {coef:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    print("="*50)
    
    train_metrics = {
        'mse': train_mse,
        'rmse': train_rmse,
        'mae': train_mae,
        'r2': train_r2
    }
    
    test_metrics = {
        'mse': test_mse,
        'rmse': test_rmse,
        'mae': test_mae,
        'r2': test_r2
    }
    
    return model, scaler, train_metrics, test_metrics

def save_model(model, encoders, scaler, filepath='models/bus_model.joblib', encoders_filepath='models/encoders.joblib', scaler_filepath='models/scaler.joblib'):
    """
    Save trained model, encoders and scaler using joblib
    
    Parameters:
    model: Trained model
    encoders (dict): Label encoders for categorical variables
    scaler: Feature scaler
    filepath (str): Path to save the model
    encoders_filepath (str): Path to save the encoders
    scaler_filepath (str): Path to save the scaler
    """
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save model
    joblib.dump(model, filepath)
    print(f"\nModel saved to {filepath}")
    
    # Save encoders
    joblib.dump(encoders, encoders_filepath)
    print(f"Encoders saved to {encoders_filepath}")
    
    # Save scaler
    joblib.dump(scaler, scaler_filepath)
    print(f"Scaler saved to {scaler_filepath}")

def save_dataset(df, filepath='data/dataset.csv'):
    """
    Save generated dataset to CSV
    
    Parameters:
    df (pd.DataFrame): Dataset to save
    filepath (str): Path to save the dataset
    """
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to {filepath}")

def main():
    """
    Main function to execute the complete pipeline
    """
    
    print("\n" + "="*50)
    print("SMART BUS ARRIVAL TIME PREDICTION SYSTEM")
    print("Tamil Nadu - Kanyakumari District")
    print("VERSION: 2.0 (Bus & Destination Based)")
    print("="*50)
    
    # Generate dataset
    df = generate_dataset(num_records=250)
    
    # Save dataset
    save_dataset(df)
    
    # Preprocess data
    X, y, encoders = preprocess_data(df)
    
    # Train model
    model, scaler, train_metrics, test_metrics = train_model(X, y)
    
    # Save model, encoders, and scaler
    save_model(model, encoders, scaler)
    
    print("\n✓ Model training and saving completed successfully!")
    print("✓ You can now run 'python app.py' to start the Flask server")
    print("\nInput Features:")
    print("  - Bus Number (BUS001 to BUS008)")
    print("  - Destination (8 locations)")
    print("  - Day of Week")
    print("  - Time Period (Morning, Afternoon, Evening, Night)")
    print("  - Stop Sequence (1-7)")

if __name__ == "__main__":
    main()
