import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb

# Read the CSV file
df = pd.read_csv('media/datasets/cleanvandata.csv')

# Fix the dates
def clean_date(date_str):
    date_str = date_str.replace('\\', '')
    if '20223' in date_str:
        date_str = date_str.replace('20223', '2023')
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

# Group data by month and sum passenger counts (if not already monthly data)
df_monthly = df.groupby(df['DATE'].dt.to_period('M'))['PAX'].sum().reset_index()
df_monthly['DATE'] = df_monthly['DATE'].dt.to_timestamp()

# Add seasonal features (month, quarter)
df_monthly['month'] = df_monthly['DATE'].dt.month
df_monthly['quarter'] = df_monthly['DATE'].dt.quarter

# Create multiple lag features (try with fewer lags to avoid empty dataset)
lag_feature_count = 6  # Reduced lag count to avoid empty dataset after filling missing values
for lag in range(1, lag_feature_count + 1):  
    df_monthly[f'lag_{lag}'] = df_monthly['PAX'].shift(lag)

# Fill missing values using backward fill
df_monthly.fillna(method='bfill', inplace=True)

# Prepare features (X) and target variable (y)
df_monthly_cleaned = df_monthly.dropna()  # Ensure no rows with missing values
X = df_monthly_cleaned.drop(columns=['DATE', 'PAX'])
y = df_monthly_cleaned['PAX']

# Use SimpleImputer to handle any remaining missing values
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Scale the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split for model validation
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror',
                             n_estimators=500,
                             learning_rate=0.05,
                             max_depth=6,
                             subsample=0.8,
                             random_state=42)

# Train the model
xgb_model.fit(X_train, y_train)

# Forecast for the next 12 months for each destination
last_row = X_scaled[-1].reshape(1, -1)  # Use the last row of data as the starting point
forecast_dates = pd.date_range(df_monthly_cleaned['DATE'].max() + pd.Timedelta(days=1), periods=12, freq='M')

# Step 1: Calculate total passenger counts for each destination over the entire period
destination_totals = df.groupby('DESTINATION')['PAX'].sum().reset_index()

# Step 2: Select the top 4 destinations with the highest passenger counts
top_4_destinations = destination_totals.nlargest(4, 'PAX')['DESTINATION']

# Step 3: Filter the original data to only include the top 4 destinations
df_top4 = df[df['DESTINATION'].isin(top_4_destinations)]

# Aggregate passenger demand per month for these top 4 destinations
df_top4_monthly = (
    df_top4.groupby([df_top4['DATE'].dt.to_period('M'), 'DESTINATION'])['PAX']
    .sum()
    .reset_index()
)
df_top4_monthly['DATE'] = df_top4_monthly['DATE'].dt.to_timestamp()

# Step 4: Plot actual and forecasted values for the top 4 destinations
plt.figure(figsize=(12, 8))

# Plot actual values for each of the top 4 destinations
for destination in top_4_destinations:
    destination_data = df_top4_monthly[df_top4_monthly['DESTINATION'] == destination]
    plt.plot(destination_data['DATE'], destination_data['PAX'], label=f"Actual - {destination}", marker='o')

    # Forecast for the next 12 months
    future_forecast = []
    for _ in range(12):
        next_prediction = xgb_model.predict(last_row)[0]
        next_prediction = max(next_prediction, 0)  # Ensure no negative values
        future_forecast.append(next_prediction)

        # Update the input row for the next prediction
        last_row = np.roll(last_row, -1)  # Shift values to the left
        last_row[0, -1] = next_prediction  # Add the new prediction as the last lag

    # Plot the forecasted values for the top 4 destinations
    plt.plot(forecast_dates, future_forecast, label=f"Forecasted - {destination}", linestyle='--', marker='x')

# Customize plot labels and title
plt.xlabel("Date")
plt.ylabel("Passenger Count")
plt.title("Actual vs Forecasted Passenger Demand for Top 4 Destinations")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Evaluate the model using MAE, RMSE, and MAPE
y_pred = xgb_model.predict(X_test)

# Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)

# Root Mean Squared Error
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Mean Absolute Percentage Error
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

# Display the error metrics
print(f"Model Evaluation Metrics:")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
