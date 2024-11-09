from admin_app.models import Driver
from customer_app.models import CustomBooking, Van
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.dateformat import format
import json


def driver_login(request):
    if request.method == 'POST':
        driver_id = request.POST['driver-id']

        # Check if the driver with this ID exists
        try:
            driver = Driver.objects.get(driver_id=driver_id)
            # If driver exists, redirect to the dashboard
            return redirect('driver_dashboard', driver_id=driver.driver_id)
        except Driver.DoesNotExist:
            # If the driver doesn't exist, display an error message
            messages.error(request, "Invalid Driver ID")
    
    return render(request, 'driver_app/driverlogin.html')

def driver_logout(request):
    logout(request)  # This logs out the user
    return redirect('driver_login')  # Redir



def driver_dashboard(request, driver_id):
    # Fetch the driver and associated bookings
    driver = Driver.objects.get(driver_id=driver_id)
    vans = Van.objects.filter(driver=driver)
    bookings = CustomBooking.objects.filter(van__in=vans)

    # Serialize the bookings into JSON format
    booking_data = serialize('json', bookings, fields=('full_name', 'pickup_datetime', 'pickup_address', 'dropoff_address', 'passenger_count', 'contact_number', 'email_address', 'round_trip', 'additional_notes'))

    # Pass the serialized booking data to the template
    context = {
        'driver': driver,
        'booking_data_json': booking_data
    }

    return render(request, 'driver_app/driverdashboard.html', context)
