import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Read the CSV file
df = pd.read_csv('media/datasets/cleanvandata.csv')

# Fix the dates
def clean_date(date_str):
    # Remove any backslashes
    date_str = date_str.replace('\\', '')
    # Fix the typo in year
    if '20223' in date_str:
        date_str = date_str.replace('20223', '2023')
    # Fix February 29 to February 28
    if '02/29/2023' in date_str:
        date_str = '02/28/2023'
    return date_str

# Apply cleaning
df['DATE'] = df['DATE'].apply(clean_date)
df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')

# Convert PAX column to integer
df['PAX'] = df['PAX'].fillna(0).astype(int)

# Sort by date
df = df.sort_values('DATE')

# Aggregate PAX per destination per month
df_monthly = (
    df.groupby([df['DATE'].dt.to_period('M'), 'DESTINATION'])['PAX']
    .sum()
    .reset_index()
)
df_monthly['DATE'] = df_monthly['DATE'].dt.to_timestamp()

# Identify the top 4 destinations by total passenger count
top_destinations = (
    df_monthly.groupby('DESTINATION')['PAX']
    .sum()
    .sort_values(ascending=False)
    .head(4)
    .index
)

# Initialize a dictionary to hold forecast results for the top 4 destinations
destination_forecasts = {}

# Initialize dictionaries to hold the metrics for each destination
metrics = {
    'MAE': {},
    'RMSE': {},
    'MAPE': {}
}

# Loop through the top 4 destinations to perform forecasting
for destination in top_destinations:
    # Filter data for the current destination
    df_dest = df_monthly[df_monthly['DESTINATION'] == destination]

    # Skip destinations with insufficient data (less than two rows)
    if len(df_dest) < 2:
        print(f"Skipping destination {destination} due to insufficient data.")
        continue

    # Create lag features (1 lag feature)
    for lag in range(1, 2):  # Using only 1 lag for simplicity
        df_dest[f'lag_{lag}'] = df_dest['PAX'].shift(lag)

    # Fill missing values using forward fill
    df_dest.fillna(method='ffill', inplace=True)

    # Drop rows with NaN values
    df_dest_cleaned = df_dest.dropna()

    # If the cleaned data is still empty, skip this destination
    if df_dest_cleaned.empty:
        print(f"Skipping destination {destination} after cleaning due to no valid data.")
        continue

    # Prepare features (X) and target variable (y)
    X = df_dest_cleaned.drop(columns=['DATE', 'PAX', 'DESTINATION'])
    y = df_dest_cleaned['PAX']

    # Use SimpleImputer to handle any remaining missing values
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    # Initialize RandomForest model
    rf_model = RandomForestRegressor(n_estimators=50, random_state=42)

    # Train the model on the destination-specific dataset
    rf_model.fit(X, y)

    # Forecast for the next 12 months for the current destination
    last_row = X.iloc[-1].values.reshape(1, -1)
    future_forecast = []
    forecast_dates = pd.date_range(df_dest_cleaned['DATE'].max() + pd.Timedelta(days=1), periods=12, freq='ME')

    for _ in range(12):
        next_prediction = rf_model.predict(last_row)[0]
        next_prediction = max(next_prediction, 0)  # Ensure no negative values
        future_forecast.append(next_prediction)

        # Update the input row for the next prediction
        last_row = np.roll(last_row, -1)  # Shift values to the left
        last_row[0, -1] = next_prediction  # Add the new prediction as the last lag

    # Store the forecast for the current destination
    destination_forecasts[destination] = pd.DataFrame({
        'DATE': forecast_dates,
        'PAX': future_forecast,
        'DESTINATION': destination
    })

    # Calculate and store metrics
    actual_values = df_dest_cleaned['PAX'].values
    predicted_values = rf_model.predict(X)

    mae = mean_absolute_error(actual_values, predicted_values)
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    mape = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100

    metrics['MAE'][destination] = mae
    metrics['RMSE'][destination] = rmse
    metrics['MAPE'][destination] = mape

# Print the metrics for each destination
print("Metrics for each destination:")
for destination in top_destinations:
    if destination in metrics['MAE']:
        print(f"\n{destination}:")
        print(f"MAE: {metrics['MAE'][destination]}")
        print(f"RMSE: {metrics['RMSE'][destination]}")
        print(f"MAPE: {metrics['MAPE'][destination]}")

# Plotting the actual and forecasted passenger counts for all top 4 destinations
plt.figure(figsize=(12, 8))

for destination in destination_forecasts:
    # Get the forecasted values for the current destination
    forecast_df = destination_forecasts[destination]

    # Plot forecasted values
    plt.plot(forecast_df['DATE'], forecast_df['PAX'], label=f"Forecasted for {destination}", linestyle='--')

plt.xlabel("Date")
plt.ylabel("Passenger Count")
plt.title("Actual vs Forecasted Passenger Demand for Top 4 Destinations")
plt.legend()
plt.grid()
plt.show()
