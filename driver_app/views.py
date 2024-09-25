from django.shortcuts import render

def driverdashboard(request):
    return render(request, 'driver_app/driverdashboard.html') 

def driverlogin(request):
    return render(request, 'driver_app/driverlogin.html') 