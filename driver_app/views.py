from admin_app.models import Driver
from django.shortcuts import render, redirect
from django.contrib import messages

def driverdashboard(request):
    return render(request, 'driver_app/driverdashboard.html') 

def driverlogin(request):
    return render(request, 'driver_app/driverlogin.html') 


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

def driver_dashboard(request, driver_id):
    # Fetch the driver object to display information on the dashboard
    driver = Driver.objects.get(driver_id=driver_id)
    return render(request, 'driver_app/driverdashboard.html', {'driver': driver})

