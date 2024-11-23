# admin_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        'destination': destinations,  # Corrected to provide a queryset
    })

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

from customer_app.models import Booking  # Import the Booking model

@login_required
def admin_bookings(request):
    query = request.GET.get('q')  # Get the search query
    # Retrieve all bookings from the database
    bookings = Booking.objects.all()  # You can add filtering or ordering if needed
    if query:
        # Filter bookings based on the search query
        bookings = bookings.filter(full_name__icontains=query)


    return render(request, 'admin_app/adminbookings.html', {'bookings': bookings})

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

def delete_van(request, van_id):
    if request.method == 'POST':
        van = get_object_or_404(Van, id=van_id)  # Get the van object
        van.delete()  # Delete the van record
        messages.success(request, 'Van deleted successfully!')  # Show success message
        return redirect('van_management')  # Redirect to the van management page

    return redirect('van_management')  # Redirect if not a POST request

def delete_destination(request, destination_id):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id)  # Get the van object
        destination.delete()  # Delete the van record
        messages.success(request, 'Destination deleted successfully!')  # Show success message
        return redirect('destination')  # Redirect to the van management page

    return redirect('destination')  # Redirect if not a POST request

from django.shortcuts import render
import pandas as pd
from prophet import Prophet

def statistics_view(request):
    # Load CSV
    df = pd.read_csv('media/datasets/FINAL_DATA.csv', names=['DATE', 'DESTINATION', 'PAX', 'AMOUNT', 'TOTAL', 'AGENCY'])
    
    # Remove header row if mixed
    df = df[df['DATE'] != 'DATE']

    # Handle invalid dates
    df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y', errors='coerce')
    df = df.dropna(subset=['DATE'])
    
    # Convert numeric columns
    df['PAX'] = pd.to_numeric(df['PAX'], errors='coerce')
    df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')
    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')

    # Drop rows with invalid PAX or TOTAL
    df = df.dropna(subset=['PAX', 'TOTAL'])

    # Group bookings by month and destination
    df['MONTH'] = df['DATE'].dt.to_period('M').dt.to_timestamp()
    actual_data = df.groupby(['MONTH', 'DESTINATION'])['PAX'].sum().reset_index()

    # Get top 10 destinations by total bookings
    top_destinations = actual_data.groupby('DESTINATION')['PAX'].sum().nlargest(10).index
    
    # Rearrange top_destinations so that charts 5-10 appear first, followed by charts 1-4
    reordered_destinations = top_destinations[4:].tolist() + top_destinations[:4].tolist()

    # Define holidays (example: you can add more or use a holiday API)
    holidays = pd.DataFrame({
        'holiday': ['New Year', 'Christmas', 'Easter'],  # Example holidays
        'ds': pd.to_datetime(['2024-01-01', '2024-12-25', '2024-04-09']),  # Example holiday dates (use the actual dates you need)
        'lower_window': 0,  # Holiday effect starts on the holiday date
        'upper_window': 1   # Holiday effect continues for one day after
    })

    # Initialize the forecasts dictionary to store forecast data
    forecasts = {}

    for destination in reordered_destinations:
        # Actual data for this destination
        dest_actual = actual_data[actual_data['DESTINATION'] == destination]
        
        # Prepare forecast data for this destination
        dest_data = df[df['DESTINATION'] == destination]
        prophet_df = pd.DataFrame({'ds': dest_data['DATE'], 'y': dest_data['PAX']}).sort_values('ds')

        if not prophet_df.empty:
            # Create and train the Prophet model
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, holidays=holidays)
            model.fit(prophet_df)

            # Calculate the number of periods until the end of 2024
            last_date = dest_data['DATE'].max()  # Get the latest date in the data
            end_of_2024 = pd.to_datetime('2024-12-31')  # Define the end of 2024
            periods = (end_of_2024 - last_date).days  # Calculate the number of days between the last date and 12/31/2024
            
            # Generate future dates for prediction until the end of 2024
            future_dates = model.make_future_dataframe(periods=periods, freq='D')  # Ensure daily frequency for the prediction
            forecast = model.predict(future_dates)

            # Combine the forecasted dates and predicted passenger numbers
            combined_data = [
                {'date': date, 'forecasted_pax': pax}
                for date, pax in zip(forecast['ds'].dt.strftime('%Y-%m-%d'), forecast['yhat'])
            ]

            # Store the forecast data in the forecasts dictionary
            forecasts[destination] = {
                'dates': forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),  # Convert datetime to string
                'yhat': forecast['yhat'].tolist(),  # Forecasted passenger numbers
                'actual_data': {str(k): v for k, v in dest_actual.set_index('MONTH')['PAX'].to_dict().items()},  # Actual PAX for the destination
                'combined_data': combined_data  # Combined list of date and forecasted pax
            }

    def calculate_total(row):
        try:
            if isinstance(row['AMOUNT'], str) and row['AMOUNT'].strip().upper() == 'PRIVATE':
                return row['TOTAL']
            else:
                return row['PAX'] * row['AMOUNT']
        except:
            return 0  # Handle any errors gracefully

    # Apply the calculation to each row
    df['calculated_total'] = df.apply(calculate_total, axis=1)

    # Group by DESTINATION for charts
    destination_summary = df.groupby('DESTINATION').agg(
        total_bookings=('PAX', 'count'),
        total_passengers=('PAX', 'sum'),
        total_revenue=('calculated_total', 'sum')
    ).reset_index()

    # Calculate total summary metrics for container boxes
    total_bookings = df['PAX'].count()
    total_passengers = df['PAX'].sum()
    total_revenue = df['calculated_total'].sum()

    # Pass the forecasts data to the HTML template
    return render(request, 'admin_app/adminstatistics.html', {
        'forecasts': forecasts,
        'total_bookings': total_bookings,
        'total_passengers': total_passengers,
        'total_revenue': total_revenue,
    })

