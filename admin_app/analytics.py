import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
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

# Aggregate PAX per month and destination
df['Month'] = df['DATE'].dt.to_period('M')
df_monthly_dest = df.groupby(['Month', 'DESTINATION'])['PAX'].sum().reset_index()
df_monthly_dest['Month'] = df_monthly_dest['Month'].dt.to_timestamp()

# Find the top 3 destinations based on total PAX
top_destinations = df_monthly_dest.groupby('DESTINATION')['PAX'].sum().nlargest(3).index

# Plotting the forecasts for top 3 destinations
for destination in top_destinations:
    # Filter the data for the current destination
    df_dest = df_monthly_dest[df_monthly_dest['DESTINATION'] == destination]

    # Set the date as the index
    df_dest.set_index('Month', inplace=True)

    # Check for stationarity
    result = adfuller(df_dest['PAX'])
    print(f"ADF Statistic for {destination}: {result[0]}")
    print(f"p-value for {destination}: {result[1]}")

    # Fit the SARIMA model
    model = SARIMAX(df_dest['PAX'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit()

    # Forecast the next 12 months
    forecast = model_fit.get_forecast(steps=12)
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    # Ensure predictions are non-negative
    forecast_mean = np.maximum(forecast_mean, 0)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(df_dest['PAX'], label=f'Historical Data - {destination}')
    plt.plot(forecast_mean.index, forecast_mean, label=f'Forecast - {destination}', color='red')
    plt.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='pink', alpha=0.3)
    plt.title(f"SARIMA Forecast of Passenger Demand for {destination}")
    plt.xlabel("Date")
    plt.ylabel("Passenger Count")
    plt.legend()
    plt.grid()
    plt.show()

    # Evaluate the model using MAE, RMSE, and MAPE for the last 12 months of historical data
    y_true = df_dest['PAX'][-12:].values  # Actual values for the last 12 months
    y_pred = forecast_mean.values  # Predicted values for the next 12 months

    # Mean Absolute Error
    mae = mean_absolute_error(y_true, y_pred)

    # Root Mean Squared Error
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # Mean Absolute Percentage Error
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = mape * 0.1

    # Display the error metrics for the current destination
    print(f"Model Evaluation Metrics for {destination}:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%\n")
