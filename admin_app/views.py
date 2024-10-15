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
def driver_management(request):
    return render(request, 'admin_app/admindriver.html')

@login_required
def statistics(request):
    return render(request, 'admin_app/adminstatistics.html')

from django.contrib import messages
from .forms import VanForm
from .models import Van

@login_required
def van_management(request):
    drivers = Driver.objects.all()  # Get all drivers
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

    vans = Van.objects.all()
    for van in vans:
        print(van.file_upload.url if van.file_upload else 'No file uploaded')  # Debugging line
    
    return render(request, 'admin_app/van_management.html', {'drivers': drivers, 'vans': vans, 'form': form})

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
        form = DriverForm(request.POST)
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
        driver_id = request.POST.get('driver_id')  # Get the custom driver ID from the form
        driver = get_object_or_404(Driver, driver_id=driver_id)  # Fetch by driver_id, not the primary key
        
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()  # Save the updated driver details
            return JsonResponse({'status': 'success', 'message': 'Driver updated successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form validation failed.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
