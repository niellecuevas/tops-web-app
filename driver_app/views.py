from admin_app.models import Driver
from customer_app.models import CustomBooking, Van
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

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
    # Fetch the driver object to display information on the dashboard
    driver = Driver.objects.get(driver_id=driver_id)
    # Fetch the vans associated with the driver
    vans = Van.objects.filter(driver=driver)
    # Fetch the bookings associated with these vans
    bookings = CustomBooking.objects.filter(van__in=vans)

    return render(request, 'driver_app/driverdashboard.html', {
        'driver': driver,
        'bookings': bookings,
    })
