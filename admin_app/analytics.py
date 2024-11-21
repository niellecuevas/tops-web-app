import pandas as pd

def process_booking_data(file_path):
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Ensure that the relevant columns are numeric
    df['PAX'] = pd.to_numeric(df['PAX'], errors='coerce')
    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')
    
    # Handle non-numeric AMOUNT values (e.g., 'PRIVATE')
    def calculate_total(row):
        try:
            # If 'AMOUNT' is not numeric (e.g., 'PRIVATE'), use 'TOTAL'
            if isinstance(row['AMOUNT'], str) and row['AMOUNT'].strip().upper() == 'PRIVATE':
                return row['TOTAL']
            else:
                # Otherwise, calculate the total as 'PAX' * 'AMOUNT'
                return row['PAX'] * row['AMOUNT']
        except:
            return 0  # In case of any errors, return 0 (could also log the error)

    # Apply the calculation function to each row
    df['calculated_total'] = df.apply(calculate_total, axis=1)

    # Group by DESTINATION and aggregate the data
    destination_summary = df.groupby('DESTINATION').agg(
        total_bookings=('PAX', 'count'),
        total_passengers=('PAX', 'sum'),
        total_revenue=('calculated_total', 'sum')
    ).reset_index()

    return destination_summary
