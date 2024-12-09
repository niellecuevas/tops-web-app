import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

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

# Check for missing values before applying imputation
print(f"Missing values in data before imputation:\n{df_monthly.isnull().sum()}")

# Fill missing values using backward fill or mean
df_monthly.fillna(method='bfill', inplace=True)  # Try bfill or use imputation strategy

# Check if there are still missing values
print(f"Missing values after filling:\n{df_monthly.isnull().sum()}")

# Prepare features (X) and target variable (y)
df_monthly_cleaned = df_monthly.dropna()  # Ensure no rows with missing values
X = df_monthly_cleaned.drop(columns=['DATE', 'PAX'])
y = df_monthly_cleaned['PAX']

# Check the shapes before proceeding
print(f"Shape of X: {X.shape}, Shape of y: {y.shape}")

# Use SimpleImputer to handle any remaining missing values
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Ensure no missing values after imputation
print(f"Missing values after imputation:\n{X.isnull().sum()}")

# Scale the features using StandardScaler (important for KNN)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Ensure the scaling step works correctly and results in a non-empty array
print(f"Shape of X_scaled: {X_scaled.shape}")

# Train-test split for model validation
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize KNN model
knn_model = KNeighborsRegressor(n_neighbors=5)  # Start with n_neighbors = 5

# Train the model
knn_model.fit(X_train, y_train)

# Forecast for the next few months (12 months)
last_row = X_scaled[-1].reshape(1, -1)  # Use the last row of data as starting point
future_forecast = []
forecast_dates = pd.date_range(df_monthly_cleaned['DATE'].max() + pd.Timedelta(days=1), periods=12, freq='M')

for _ in range(12):
    next_prediction = knn_model.predict(last_row)[0]
    next_prediction = max(next_prediction, 0)  # Ensure no negative values
    future_forecast.append(next_prediction)

    # Update the input row for the next prediction
    last_row = np.roll(last_row, -1)  # Shift values to the left
    last_row[0, -1] = next_prediction  # Add the new prediction as the last lag

# Display forecasted values for the next 12 months
print("Forecasted Passenger Demand for the Next 12 Months:")
for i, value in enumerate(future_forecast, 1):
    print(f"Month {i}: {value:.2f}")

# Evaluate the model using MAE, RMSE, and MAPE
y_pred = knn_model.predict(X_test)

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

# Plot actual vs predicted values (using the cleaned data and the forecasted data)
plt.figure(figsize=(10, 6))
plt.plot(df_monthly_cleaned['DATE'], y, label="Actual", marker='o', color='blue')
plt.plot(forecast_dates, future_forecast, label="Forecasted", marker='o', linestyle='--', color='red')
plt.xlabel("Date")
plt.ylabel("Passenger Count")
plt.title("Actual vs Forecasted Passenger Demand")
plt.legend()
plt.grid()
plt.show()
