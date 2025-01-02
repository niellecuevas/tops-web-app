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

    

    # Optional debugging: Print URLs of uploaded files for all destinations
    for dest in destinations:
        print(dest.file_upload.url if dest.file_upload else 'No file uploaded')

    return render(request, 'admin_app/destination.html', {
        'form': form,
        'destination': destinations, 
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
    query = request.GET.get('q')  # Get the search query from the URL
    
    # Filter `Booking` entries by status
    pending_bookings = Booking.objects.filter(status='Pending')
    confirmed_bookings = Booking.objects.filter(status='Confirmed')
    cancelled_bookings = Booking.objects.filter(status='Cancelled')
    
    # Filter `CustomBooking` entries by status
    pending_custom_bookings = CustomBooking.objects.filter(custom_status='Pending')
    confirmed_custom_bookings = CustomBooking.objects.filter(custom_status='Confirmed')
    cancelled_custom_bookings = CustomBooking.objects.filter(custom_status='Cancelled')

    # Apply search query to both Booking and CustomBooking models
    if query:
        pending_bookings = pending_bookings.filter(full_name__icontains=query)
        confirmed_bookings = confirmed_bookings.filter(full_name__icontains=query)
        cancelled_bookings = cancelled_bookings.filter(full_name__icontains=query)
        pending_custom_bookings = pending_custom_bookings.filter(full_name__icontains=query)
        confirmed_custom_bookings = confirmed_custom_bookings.filter(full_name__icontains=query)
        cancelled_custom_bookings = cancelled_custom_bookings.filter(full_name__icontains=query)

    return render(request, 'admin_app/adminbookings.html', {
        'pending_custom_bookings': pending_custom_bookings,
        'confirmed_custom_bookings': confirmed_custom_bookings,
        'cancelled_custom_bookings': cancelled_custom_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
    })


def confirm_booking(request, booking_id):
    # Confirm a standard booking
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Confirmed'  # Change status to "Confirmed"
    booking.save()
    return redirect('admin_bookings')

def cancel_booking(request, booking_id):
    # Cancel a booking
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'  # Change status to "Cancelled"
    booking.save()
    return redirect('admin_bookings')

def confirm_custom_booking(request, booking_id):
    # Confirm a custom booking
    custom_booking = get_object_or_404(CustomBooking, id=booking_id)
    custom_booking.custom_status = 'Confirmed'  # Change custom_status to "Confirmed"
    custom_booking.save()
    return redirect('admin_bookings')

def cancel_custom_booking(request, booking_id):
    # Cancel a booking
    custom_booking = get_object_or_404(CustomBooking, id=booking_id)
    custom_booking.custom_status = 'Cancelled'  # Change status to "Cancelled"
    custom_booking.save()
    return redirect('admin_bookings')

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

from django.shortcuts import render
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

def statistics_view(request):
     # 1. Load historical data from the CSV file
    historical_data = pd.read_csv('media/datasets/cleanvandata.csv')

    # Clean DATE column in CSV
    def clean_date(date_str):
        date_str = date_str.replace('\\', '')
        if '20223' in date_str:
            date_str = date_str.replace('20223', '2023')
        if '02/29/2023' in date_str:
            date_str = '02/28/2023'
        return date_str

    historical_data['DATE'] = historical_data['DATE'].apply(clean_date)
    historical_data['DATE'] = pd.to_datetime(historical_data['DATE'], format='%m/%d/%Y')
    historical_data['PAX'] = historical_data['PAX'].fillna(0).astype(int)

    # Add REVENUE column based on TYPE
    historical_data['REVENUE'] = np.where(
        historical_data['TYPE'] == 'SHARED',
        historical_data['PAX'] * 500,  # Shared: PAX * 500
        historical_data['COST']  # Private: Fixed cost
    )

    # 2. Fetch real-time booking data from the database
    booking_data = Booking.objects.filter(status='Confirmed')  # Use only confirmed bookings
    real_time_data = pd.DataFrame(list(booking_data.values('passenger_count', 'pickup_datetime', 'destination')))

    # Rename columns to match historical data
    if not real_time_data.empty:
        real_time_data.rename(columns={
            'passenger_count': 'PAX',
            'pickup_datetime': 'DATE',
            'destination': 'DESTINATION'
        }, inplace=True)

        # Add TYPE and REVENUE columns for real-time data
        real_time_data['TYPE'] = 'PRIVATE'  # Assume all database bookings are private
        real_time_data['COST'] = 0  # Default cost for dynamic pricing calculation
        real_time_data['REVENUE'] = 0  # Placeholder for revenue (calculated later)
        real_time_data['DATE'] = pd.to_datetime(real_time_data['DATE'])

    # 3. Combine historical and real-time data
    combined_data = pd.concat([historical_data, real_time_data], ignore_index=True)
    combined_data['DATE'] = pd.to_datetime(combined_data['DATE'], errors='coerce')
    combined_data['Month'] = combined_data['DATE'].dt.to_period('M')


    # Aggregate revenue by destination
    df_revenue = combined_data.groupby('DESTINATION')['REVENUE'].sum().reset_index()

    # Get the top 5 destinations based on revenue
    top_destinations = df_revenue.nlargest(5, 'REVENUE')
    current_month = datetime.now().strftime('%Y-%m')

    # Filter for 'PRIVATE' type bookings for dynamic pricing
    private_df = combined_data[combined_data['TYPE'] == 'PRIVATE']

    dynamic_pricing_data = []

    from matplotlib.ticker import FuncFormatter

    # Custom currency format for the y-axis
    def currency_format(x, pos):
        return f'₱{x:,.0f}'

    # Create bar chart for top 5 destinations
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_destinations['DESTINATION'], top_destinations['REVENUE'], color='#CDC1FF')
    ax.set_title('Top 5 Destinations by Revenue')
    ax.set_xlabel('Destination')
    ax.set_ylabel('Revenue (₱)')
    ax.grid(True)

    # Apply the custom formatter to the y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(currency_format))

    # Convert plot to base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    revenue_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Aggregate the number of successful trips by agency
    df_agency_trips = combined_data.groupby('AGENCY').size().reset_index(name='TRIPS')

    # Get the top 6 agencies based on the number of successful trips
    top_agencies = df_agency_trips.nlargest(6, 'TRIPS')

    # Create horizontal bar chart for top 6 agencies
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_agencies['AGENCY'], top_agencies['TRIPS'], color='#FFCCE1')
    ax.set_title('Top 6 Agencies by Successful Trips')
    ax.set_xlabel('Number of Trips')
    ax.set_ylabel('Agency')
    ax.grid(True)

    # Convert horizontal bar chart to base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    agency_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Descriptive analytics
    total_revenue = combined_data['REVENUE'].sum()  # Total revenue
    total_destinations = combined_data['DESTINATION'].nunique()  # Total unique destinations
    total_agencies = combined_data['AGENCY'].nunique()  # Total unique agencies
    total_trips = len(combined_data)  # Total trips made

    # Aggregate PAX per month and destination
    combined_data['Month'] = combined_data['DATE'].dt.to_period('M')
    df_monthly_dest = combined_data.groupby(['Month', 'DESTINATION'])['PAX'].sum().reset_index()
    df_monthly_dest['Month'] = df_monthly_dest['Month'].dt.to_timestamp()

    # Find the top 3 destinations based on total PAX
    top_destinations = df_monthly_dest.groupby('DESTINATION')['PAX'].sum().nlargest(3).index

    forecasts = []

    dynamic_pricing_all_dest = []

    # Loop over all unique destinations for dynamic pricing
    all_destinations = private_df['DESTINATION'].unique()

    for destination in all_destinations:
        # Filter data for the current destination
        df_dest = df_monthly_dest[df_monthly_dest['DESTINATION'] == destination]
        df_dest.set_index('Month', inplace=True)

        # Forecasting using SARIMA for the top 3 destinations
        if destination in top_destinations:
            # Fit the SARIMA model for the top destinations
            model = SARIMAX(df_dest['PAX'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            model_fit = model.fit()

            # Forecast the next 12 months
            forecast = model_fit.get_forecast(steps=12)
            forecast_mean = forecast.predicted_mean
            forecast_ci = forecast.conf_int()

            # Ensure predictions are non-negative
            forecast_mean = np.maximum(forecast_mean, 0)

            # Create plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_dest['PAX'], label=f'Historical Data - {destination}')
            ax.plot(forecast_mean.index, forecast_mean, label=f'Forecast - {destination}', color='red')
            ax.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='pink', alpha=0.3)
            ax.set_title(f"SARIMA Forecast of Passenger Demand for {destination}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Passenger Count")
            ax.legend()
            ax.grid()

            # Convert plot to base64
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            # Append the forecast image
            forecasts.append({
                'destination': destination,
                'forecast_image': img_base64,
            })

        # Calculate dynamic pricing adjustment for private trips
        private_dest_data = private_df[private_df['DESTINATION'] == destination]
        private_latest_price = private_dest_data['COST'].iloc[-1] if not private_dest_data.empty else 0

        avg_demand = df_dest['PAX'].mean()
        price_adjustment = 1  # Default to no adjustment

        # Dynamic pricing logic based on forecasted demand
        if destination in all_destinations:
            for month, demand in forecast_mean.items():
                if month.strftime('%Y-%m') == current_month:
                    price_adjustment = 1.20  # Increase by 20%
                elif demand > avg_demand and month.strftime('%Y-%m') == current_month:
                    price_adjustment = 0.90  # Decrease by 10%

            dynamic_price = private_latest_price * price_adjustment if private_latest_price > 0 else 0

            # Append the dynamic price data for the current destination
            dynamic_pricing_all_dest.append({
                'destination': destination,
                'current_month': current_month,
                'dynamic_price': dynamic_price,
                'original_price': private_latest_price
            })

            # Sort dynamic_pricing_all_dest by dynamic_price in descending order
            dynamic_pricing_all_dest = sorted(
                dynamic_pricing_all_dest,
                key=lambda x: x['dynamic_price'],  # Sort by dynamic price
                reverse=True  # Descending order
            )

            # Limit to the top 20 destinations
            dynamic_pricing_all_dest = dynamic_pricing_all_dest[:20]

    # Pass analytics and forecasts to the template
    context = {
        'forecasts': forecasts,
        'total_revenue': total_revenue,
        'total_destinations': total_destinations,
        'total_agencies': total_agencies,
        'total_trips': total_trips,
        'revenue_chart': revenue_chart_base64,
        'agency_chart': agency_chart_base64,
        'dynamic_pricing_data': dynamic_pricing_data,
        'dynamic_pricing_all_dest': dynamic_pricing_all_dest
    }

    return render(request, 'admin_app/adminstatistics.html', context)

