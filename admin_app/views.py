# admin_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password.'
            return render(request, 'admin_app/adminlogin.html', {'error': error})
    
    return render(request, 'admin_app/adminlogin.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_app/admindashboard.html')

@login_required
def bookings(request):
    return render(request, 'admin_app/adminbookings.html')

@login_required
def driver_management(request):
    return render(request, 'admin_app/admindriver.html')

@login_required
def statistics(request):
    return render(request, 'admin_app/adminstatistics.html')

@login_required
def logout(request):
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login


from .forms import DriverForm
from .models import Driver

def driver_management(request):
    # Handle form submission
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new driver to the database
            return redirect('driver_management')  # Redirect to the same page after successful registration
    else:
        form = DriverForm()  # Empty form if no form submission

    # Fetch all drivers to display in the list
    drivers = Driver.objects.all()

    # Pass both the form and the driver list to the template
    return render(request, 'admin_app/driver_management.html', {'form': form, 'drivers': drivers})
