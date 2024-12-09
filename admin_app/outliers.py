import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Aggregate PAX per month across all destinations
df_monthly = df.groupby(df['DATE'].dt.to_period('M'))['PAX'].sum().reset_index()
df_monthly['DATE'] = df_monthly['DATE'].dt.to_timestamp()

# Set the date as the index
df_monthly.set_index('DATE', inplace=True)

# Outlier Detection using IQR
Q1 = df_monthly['PAX'].quantile(0.25)
Q3 = df_monthly['PAX'].quantile(0.75)
IQR = Q3 - Q1

# Define bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = df_monthly[(df_monthly['PAX'] < lower_bound) | (df_monthly['PAX'] > upper_bound)]

# Print outliers
print("Detected Outliers:")
print(outliers)

# Optionally, visualize the outliers
plt.figure(figsize=(10, 6))
plt.plot(df_monthly['PAX'], label='Passenger Count', color='blue')
plt.scatter(outliers.index, outliers['PAX'], color='red', label='Outliers', marker='o')
plt.axhline(y=upper_bound, color='green', linestyle='--', label='Upper Bound')
plt.axhline(y=lower_bound, color='orange', linestyle='--', label='Lower Bound')
plt.title("Passenger Count with Outliers Highlighted")
plt.xlabel("Date")
plt.ylabel("Passenger Count")
plt.legend()
plt.grid()
plt.show()