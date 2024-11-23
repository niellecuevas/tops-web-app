# Convert DATE to datetime and clean the data
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('media/datasets/FINAL_DATA.csv')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert DATE to datetime
df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y', errors='coerce')

# Convert PAX and TOTAL to numeric
df['PAX'] = pd.to_numeric(df['PAX'], errors='coerce')
df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')

# Display basic information about the dataset
print("Dataset Overview:")
print(df.head())
print("\
Basic Statistics:")
print(df.describe())

# Plotting the monthly passenger trends for top 5 destinations
plt.figure(figsize=(12, 6))
df['Month'] = df['DATE'].dt.to_period('M')
monthly_pax = df.groupby(['Month', 'DESTINATION'])['PAX'].sum().reset_index()
top_5_destinations = df.groupby('DESTINATION')['PAX'].sum().nlargest(5).index

plt.figure(figsize=(12, 6))
for dest in top_5_destinations:
    dest_data = monthly_pax[monthly_pax['DESTINATION'] == dest]
    plt.plot(dest_data['Month'].astype(str), dest_data['PAX'], label=dest, marker='o')

plt.title('Monthly Passenger Trends for Top 5 Destinations')
plt.xticks(rotation=45)
plt.xlabel('Month')
plt.ylabel('Number of Passengers')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# Complete analytics pipeline for Django integration
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime, timedelta
import base64
from io import BytesIO

class TransportAnalytics:
    def __init__(self):
        self.df = pd.read_csv('FINAL_DATA.csv')
        self.df_clean = None
        self.forecasts = {}
        self.visualization_data = {}
        
    def clean_data(self):
        # Convert DATE to datetime
        self.df['DATE'] = pd.to_datetime(self.df['DATE'])
        
        # Clean numerical columns
        self.df['PAX'] = pd.to_numeric(self.df['PAX'], errors='coerce')
        
        # Remove missing values
        self.df_clean = self.df.dropna(subset=['DATE', 'PAX', 'DESTINATION'])
        
        # Sort by date
        self.df_clean = self.df_clean.sort_values('DATE')
        
        print("Data cleaning complete")
        print(f"Original rows: {len(self.df)}")
        print(f"Cleaned rows: {len(self.df_clean)}")
        return self.df_clean
    
    def generate_forecasts(self, forecast_days=30):
        # Get top 5 destinations by volume
        top_destinations = self.df_clean.groupby('DESTINATION')['PAX'].sum().nlargest(5).index
        
        for dest in top_destinations:
            # Prepare data for this destination
            dest_data = self.df_clean[self.df_clean['DESTINATION'] == dest].copy()
            
            # Resample to daily frequency and fill gaps
            daily_data = dest_data.set_index('DATE')['PAX'].resample('D').mean().fillna(method='ffill')
            
            # Fit model
            model = ExponentialSmoothing(daily_data,
                                       seasonal_periods=7,  # Weekly seasonality
                                       trend='add',
                                       seasonal='add')
            fitted_model = model.fit()
            
            # Generate forecast
            forecast = fitted_model.forecast(forecast_days)
            
            # Store results
            self.forecasts[dest] = {
                'dates': forecast.index.strftime('%Y-%m-%d').tolist(),
                'values': forecast.values.tolist(),
                'historical_dates': daily_data.index.strftime('%Y-%m-%d').tolist(),
                'historical_values': daily_data.values.tolist()
            }
        
        return self.forecasts
    
    def create_visualizations(self):
        for dest in self.forecasts.keys():
            # Create figure
            plt.figure(figsize=(12, 6))
            
            # Plot historical data
            plt.plot(pd.to_datetime(self.forecasts[dest]['historical_dates']), 
                    self.forecasts[dest]['historical_values'],
                    label='Historical', color='blue')
            
            # Plot forecast
            plt.plot(pd.to_datetime(self.forecasts[dest]['dates']),
                    self.forecasts[dest]['values'],
                    label='Forecast', color='red', linestyle='--')
            
            plt.title(f'Passenger Forecast for {dest}')
            plt.xlabel('Date')
            plt.ylabel('Number of Passengers')
            plt.legend()
            plt.grid(True)
            
            # Save plot to BytesIO object
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            # Store base64 encoded image
            self.visualization_data[dest] = base64.b64encode(image_png).decode()
            
            plt.close()
        
        return self.visualization_data
    
    def get_summary_stats(self):
        summary_stats = {}
        for dest in self.forecasts.keys():
            forecast_values = np.array(self.forecasts[dest]['values'])
            summary_stats[dest] = {
                'average': float(np.mean(forecast_values)),
                'max': float(np.max(forecast_values)),
                'min': float(np.min(forecast_values))
            }
        return summary_stats

# Initialize and run the analytics
analytics = TransportAnalytics()
analytics.clean_data()
analytics.generate_forecasts()
analytics.create_visualizations()
summary_stats = analytics.get_summary_stats()

# Print summary statistics
print("\
Forecast Summary Statistics:")
print(json.dumps(summary_stats, indent=2))

# Save the results to files that can be used by Django
with open('forecast_data.json', 'w') as f:
    json.dump(analytics.forecasts, f)
    
with open('visualization_data.json', 'w') as f:
    json.dump(analytics.visualization_data, f)
    
print("\
Files saved successfully. You can now use these in your Django application.")