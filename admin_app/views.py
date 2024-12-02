# admin_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_app.models import Destination  # Import Destination from admin_app
from customer_app.models import Booking  # Import Booking from customer_app
from django.db.models import Sum


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('statistics')
        else:
            error = 'Invalid username or password.'
            return render(request, 'admin_app/adminlogin.html', {'error': error})
    
    return render(request, 'admin_app/adminlogin.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_app/admin_dashboard.html')

@login_required
def driver_management(request):
    return render(request, 'admin_app/admindriver.html')

from .forms import DestinationForm
from .models import Destination  # Ensure you have imported your Destination model

@login_required
def destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination added successfully!')
            form = DestinationForm()  # Reset the form
            return redirect('destination')
        else:
            print(form.errors)
            messages.error(request, 'There was an error adding a destination.')
    else:
        form = DestinationForm()  # Use the correct form on GET requests

    # Query all Destination instances
    destinations = Destination.objects.all()

    # Prepare a list to store price calculations
    pricing_data = []

    for destination in destinations:
        # Get forecasted passenger count
        forecasted_pax = Booking.objects.filter(destination=destination).aggregate(Sum('passenger_count'))['passenger_count__sum'] or 0
        
        # Calculate dynamic price
        dynamic_price = calculate_dynamic_price(destination.base_price, forecasted_pax)

        # Store the result in a list
        pricing_data.append({
            'destination': destination,
            'forecasted_pax': forecasted_pax,
            'base_price': destination.base_price,
            'dynamic_price': dynamic_price
        })

    # Optional debugging: Print URLs of uploaded files for all destinations
    for dest in destinations:
        print(dest.file_upload.url if dest.file_upload else 'No file uploaded')

    return render(request, 'admin_app/destination.html', {
        'form': form,
        'destination': destinations, 
        'pricing_data': pricing_data,
    })

def update_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)  # Ensure the destination exists
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination updated successfully.')
            return redirect('destination')  # Redirect back to destination page
        else:
            messages.error(request, 'There was an error updating the destination.')
    else:
        form = DestinationForm(instance=destination)

    return render(request, 'admin_app/destination.html', {'form': form, 'destination': [destination]})

@login_required
def statistics(request):
    return render(request, 'admin_app/adminstatistics.html')


from .forms import VanForm
from .models import Van

@login_required
def van_management(request):
    drivers = Driver.objects.all()  # Get all drivers
    company_vans = Van.objects.filter(is_company_van=True)  # Get all company vans
    driver_vans = Van.objects.filter(is_company_van=False)  # Get all driver vans
    if request.method == 'POST':
        form = VanForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()  # Save the new van record
            messages.success(request, 'Van registered successfully!')
            form = VanForm()  # Reset the form
            return redirect('van_management')  # Redirect to the same view or a different one
        else:
            print(form.errors)
            messages.error(request, 'There was an error registering the van.')
    else:
        form = VanForm()  # Create a new form instance for GET requests

     # Debugging: Print URLs of uploaded files for all vans
    for van in company_vans:
        print(van.file_upload.url if van.file_upload else 'No file uploaded')  # For company vans
    for van in driver_vans:
        print(van.file_upload.url if van.file_upload else 'No file uploaded')  # For driver vans
    
    return render(request, 'admin_app/van_management.html', {'drivers': drivers, 'form': form, 'company_vans': company_vans,
        'driver_vans': driver_vans,})

@login_required
def logout(request):
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login


from .forms import DriverForm
from .models import Driver
from django.contrib import messages

@login_required
def driver_management(request):
    # Handle form submission
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new driver to the database
            messages.success(request, 'Driver registered successfully!')
            form = DriverForm()
            return redirect('driver_management')  # Redirect to the same page after successful registration
    else:
        form = DriverForm()  # Empty form if no form submission

    # Fetch all drivers to display in the list
    drivers = Driver.objects.all()

    # Pass both the form and the driver list to the template
    return render(request, 'admin_app/driver_management.html', {'form': form, 'drivers': drivers})


# admin_app/views.py

from customer_app.models import Booking, CustomBooking  # Import the Booking model

@login_required
def admin_bookings(request):
    query = request.GET.get('q')  # Get the search query
    # Retrieve all bookings from the database
    bookings = Booking.objects.all()  
    custombookings = CustomBooking.objects.all()
    if query:
        # Filter bookings based on the search query
        bookings = bookings.filter(full_name__icontains=query)


    return render(request, 'admin_app/adminbookings.html', {'bookings': bookings,'custombookings': custombookings})

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def updateDriverForm(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = Driver.objects.get(driver_id=driver_id)
        
        form = DriverForm(request.POST, request.FILES, instance=driver)  # Use request.FILES for file handling
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Driver updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to update driver details.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_driver(request, driver_id):
    if request.method == 'POST':
        driver = get_object_or_404(Driver, driver_id=driver_id)  # Get the driver object
        driver.delete()  # Delete the driver record
        messages.success(request, 'Driver deleted successfully!')  # Show success message
        return redirect('driver_management')  # Redirect to the driver management page

    return redirect('driver_management')

def delete_van(request, van_id):
    if request.method == 'POST':
        van = get_object_or_404(Van, id=van_id)  # Get the van object
        van.delete()  # Delete the van record
        messages.success(request, 'Van deleted successfully!')  # Show success message
        return redirect('van_management')  # Redirect to the van management page

    return redirect('van_management')  # Redirect if not a POST request

def update_van(request, van_id):
    van = get_object_or_404(Van, id=van_id)  # Ensure the destination exists
    
    if request.method == 'POST':
        form = VanForm(request.POST, request.FILES, instance=van)
        if form.is_valid():
            form.save()
            messages.success(request, 'Van updated successfully.')
            return redirect('van_management')  # Redirect back to destination page
        else:
            messages.error(request, 'There was an error updating the destination.')
    else:
        form = VanForm(instance=van_management)

    return render(request, 'admin_app/van_management.html', {'form': form, 'van': [van]})


def delete_destination(request, destination_id):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id)  # Get the van object
        destination.delete()  # Delete the van record
        messages.success(request, 'Destination deleted successfully!')  # Show success message
        return redirect('destination')  # Redirect to the van management page

    return redirect('destination')  # Redirect if not a POST request

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from django.shortcuts import render
import pandas as pd
from prophet import Prophet

# Utility function to calculate dynamic pricing based on forecasted demand
def calculate_dynamic_price(base_price, forecasted_pax):
    try:
        if forecasted_pax < 50:  # Low demand
            return base_price * 0.9  # 10% discount
        elif 50 <= forecasted_pax <= 100:  # Moderate demand
            return base_price  # No change
        else:  # High demand
            return base_price * 1.2  # 20% increase
    except Exception as e:
        print(f"Error in dynamic pricing calculation: {e}")
        return base_price  # Fallback to base price

# View function for generating and rendering statistics
def statistics_view(request):
    # =============================
    # 1. Load and Preprocess Data
    # =============================

    # Load CSV file
    df = pd.read_csv('media/datasets/final_data.csv', names=['DATE', 'DESTINATION', 'PAX', 'AMOUNT', 'TOTAL', 'AGENCY'])

    # Remove header row if mixed and handle invalid dates
    df = df[df['DATE'] != 'DATE']
    df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y', errors='coerce')
    df = df.dropna(subset=['DATE'])

    # Convert numeric columns and drop rows with invalid data
    df['PAX'] = pd.to_numeric(df['PAX'], errors='coerce')
    df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')
    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')
    df = df.dropna(subset=['PAX', 'TOTAL'])

    # Group bookings by month and destination
    df['MONTH'] = df['DATE'].dt.to_period('M').dt.to_timestamp()
    actual_data = df.groupby(['MONTH', 'DESTINATION'])['PAX'].sum().reset_index()

    # Identify top 10 destinations
    top_destinations = actual_data.groupby('DESTINATION')['PAX'].sum().nlargest(10).index
    reordered_destinations = top_destinations[4:].tolist() + top_destinations[:4].tolist()

    # =============================
    # 2. Define Holidays for Forecasting
    # =============================

    holidays = pd.DataFrame({
        'holiday': ['New Year', 'Christmas', 'Easter'],
        'ds': pd.to_datetime(['2024-01-01', '2024-12-25', '2024-04-09']),
        'lower_window': 0,
        'upper_window': 1
    })

    # =============================
    # 3. Forecasting and Visualization Data
    # =============================

    forecasts = {}  # To store forecast data

    # Lists to store overall forecasted and actual values
    all_forecasted_pax = []
    all_actual_pax_values = []
    all_mape_values = []

    default_base_price = 1800  # Default base price
    base_prices = {
        destination: default_base_price for destination in df['DESTINATION'].unique()
    }
    base_prices.update({'PPC-EN': 5000, 'EN-PPC': 5000, 'MILAN': 5000, 'FRENDZ': 1800})

    for destination in reordered_destinations:
        dest_actual = actual_data[actual_data['DESTINATION'] == destination]
        dest_data = df[df['DESTINATION'] == destination]
        prophet_df = pd.DataFrame({'ds': dest_data['DATE'], 'y': dest_data['PAX']}).sort_values('ds')

        if not prophet_df.empty:
            # Train Prophet model
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, holidays=holidays)
            model.fit(prophet_df)

            # Generate future dates for prediction
            last_date = dest_data['DATE'].max()
            periods = (pd.to_datetime('2024-12-31') - last_date).days
            future_dates = model.make_future_dataframe(periods=periods, freq='D')
            forecast = model.predict(future_dates)

            base_price = base_prices.get(destination, default_base_price)
            combined_data = [
                {
                    'date': date,
                    'forecasted_pax': pax,
                    'dynamic_price': calculate_dynamic_price(base_price, pax)
                }
                for date, pax in zip(forecast['ds'].dt.strftime('%Y-%m-%d'), forecast['yhat'])
            ]

            forecasts[destination] = {
                'dates': forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
                'yhat': forecast['yhat'].tolist(),
                'actual_data': {str(k): v for k, v in dest_actual.set_index('MONTH')['PAX'].to_dict().items()},
                'combined_data': combined_data,
                'base_price': base_price,
            }
# Now we calculate the accuracy (MAE) for the model prediction
            # Ensure that we have the actual PAX values for the forecasted dates
            forecast_dates = forecast['ds'].dt.strftime('%Y-%m-%d').tolist()
            forecasted_pax = forecast['yhat'].tolist()

            # Actual PAX values from the dataset for the forecasted dates
            actual_pax_values = [dest_actual[dest_actual['MONTH'] == pd.to_datetime(date)].iloc[0]['PAX'] if not dest_actual[dest_actual['MONTH'] == pd.to_datetime(date)].empty else 0 for date in forecast_dates]

            # Append to the overall lists
            all_forecasted_pax.extend(forecasted_pax)
            all_actual_pax_values.extend(actual_pax_values)

            # Calculate Mean Absolute Error (MAE) and RMSE for this destination
            mae = mean_absolute_error(actual_pax_values, forecasted_pax)
            rmse = np.sqrt(mean_squared_error(actual_pax_values, forecasted_pax))
            # Calculate MAPE for this destination
            mape = np.mean([abs((true - forecasted) / true) * 100 if true != 0 else 0 for true, forecasted in zip(actual_pax_values, forecasted_pax)])

            # Append MAPE to the list
            all_mape_values.append(mape)


            # Store the accuracy metrics for each destination
            forecasts[destination]['mae'] = mae
            forecasts[destination]['rmse'] = rmse
            forecasts[destination]['mape'] = mape

            print(f"Accuracy for {destination} - MAE: {mae}, RMSE: {rmse}, MAPE: {mape}")

    # Prepare visualization data
    visualization_data = [
        {
            'destination': destination,
            'dynamic_price': calculate_dynamic_price(
                base_prices.get(destination, default_base_price),
                sum([entry['forecasted_pax'] for entry in data['combined_data']])
            ),
            'base_price': base_prices.get(destination, default_base_price),
            'forecasted_pax': sum([entry['forecasted_pax'] for entry in data['combined_data']])
        }
        for destination, data in forecasts.items()
    ]

    # Calculate overall accuracy for all forecasts
    overall_mae = mean_absolute_error(all_actual_pax_values, all_forecasted_pax)
    overall_rmse = np.sqrt(mean_squared_error(all_actual_pax_values, all_forecasted_pax))
    overall_mape = np.mean(all_mape_values)
    
    print(f"Overall Accuracy - MAE: {overall_mae}, RMSE: {overall_rmse}, MAPE: {overall_mape}")

    # =============================
    # 4. Store Specific Data in Session
    # =============================

    for key in ['PPC-EN', 'MILAN', 'FRENDZ']:
        specific_data = next((item for item in visualization_data if item['destination'] == key), None)
        if specific_data:
            request.session[f'{key.lower()}_data'] = specific_data
        else:
            print(f"No data found for {key}.")

    # =============================
    # 5. Calculate Totals and Summaries
    # =============================

    def calculate_total(row):
        try:
            if isinstance(row['AMOUNT'], str) and row['AMOUNT'].strip().upper() == 'PRIVATE':
                return row['TOTAL']
            else:
                return row['PAX'] * row['AMOUNT']
        except:
            return 0

    df['calculated_total'] = df.apply(calculate_total, axis=1)
    destination_summary = df.groupby('DESTINATION').agg(
        total_bookings=('PAX', 'count'),
        total_passengers=('PAX', 'sum'),
        total_revenue=('calculated_total', 'sum')
    ).reset_index()

    total_bookings = df['PAX'].count()
    total_passengers = df['PAX'].sum()
    total_revenue = df['calculated_total'].sum()

    # =============================
    # 6. Render the Template
    # =============================

    labels = [item['destination'] for item in visualization_data]
    data = [item['dynamic_price'] for item in visualization_data]
    base_prices_list = [item['base_price'] for item in visualization_data]
    forecasted_pax = [item['forecasted_pax'] for item in visualization_data]

    return render(request, 'admin_app/adminstatistics.html', {
        'overall_mae': overall_mae,
        'overall_rmse': overall_rmse,
        'visualization_data': visualization_data,
        'labels': labels,
        'data': data,
        'base_prices': base_prices_list,
        'forecasted_pax': forecasted_pax,
        'forecasts': forecasts,
        'total_bookings': total_bookings,
        'total_passengers': total_passengers,
        'total_revenue': total_revenue,
    })
