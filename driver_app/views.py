from admin_app.models import Driver, Van
from customer_app.models import CustomBooking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # If you are using CSRF tokens
from django.core.serializers import serialize
from django.utils.dateformat import format
from django.contrib.auth import login
from django.core.mail import send_mail
from django.core.cache import cache  # Store OTP temporarily
import random
import json


def signup(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            # Check if the driver ID exists in the database
            driver = Driver.objects.get(driver_id=driver_id)

            # If driver ID exists, allow them to create a new account
            if driver.email:  # If email already exists, show error
                return render(request, 'driver_app/signup.html', {'error': 'This email already exists for this Driver ID.'})

            # Check password confirmation
            if password != confirm_password:
                return render(request, 'driver_app/signup.html', {'error': 'Passwords do not match.'})

            # Save the email and hashed password for the existing driver ID
            driver.email = email
            driver.set_password(password)
            driver.save()
            return redirect('driver_app:driver_login')  # Redirect to login after successful sign-up

        except Driver.DoesNotExist:
            # If the driver ID does not exist in the database, show an error message
            return render(request, 'driver_app/signup.html', {'error': 'Invalid Driver ID.'})

    return render(request, 'driver_app/signup.html')

def driver_logout(request):
    logout(request)  # Logs out the user
    return redirect('driver_app:driver_login')  # Redirect to login page

def driver_login(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        password = request.POST.get('password')

        try:
            driver = Driver.objects.get(driver_id=driver_id)
            if driver.check_password(password):
                # Log in the driver (you can use Django's login for sessions if needed)
                request.session['driver_id'] = driver_id
                # Redirect to the driver dashboard with driver_id
                return redirect('driver_app:driver_dashboard', driver_id=driver_id)
            else:
                return render(request, 'driver_app/driver_login.html', {'error': 'Invalid credentials.'})

        except Driver.DoesNotExist:
            return render(request, 'driver_app/driver_login.html', {'error': 'Driver ID not found.'})

    return render(request, 'driver_app/driver_login.html')


def send_otp_email(email):
    otp = random.randint(100000, 999999)  # Generate 6-digit OTP
    subject = 'Password Reset OTP'
    message = f'Your OTP is {otp}. Please use it to reset your password.'
    send_mail(subject, message, 'your_email@example.com', [email])  # Update sender email
    cache.set(f'otp_{email}', otp, timeout=300)
    return otp

# forgot_password view
def forgot_password(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        try:
            driver = Driver.objects.get(driver_id=driver_id)
            otp = send_otp_email(driver.email)
            cache.set(f'otp_{driver.email}', otp, timeout=300)  # OTP valid for 5 minutes
            request.session['driver_email'] = driver.email  # Store email in session
            return render(request, 'driver_app/verify_otp.html', {'email': driver.email})
        except Driver.DoesNotExist:
            return render(request, 'driver_app/forgot_password.html', {'error': 'Invalid Driver ID.'})

    return render(request, 'driver_app/forgot_password.html')

def verify_otp(request):
    email = request.session.get('driver_email')  # Retrieve email from session
    if not email:  # If email is not in session, redirect back to forgot password
        return redirect('driver_app:forgot_password')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')  # Retrieve OTP from form
        otp_stored = cache.get(f'otp_{email}')  # Get OTP from cache

        # Debugging: Log OTP comparison
        print(f"Input OTP: {otp_input}, Stored OTP: {otp_stored}")
        
        if otp_stored and str(otp_stored) == otp_input:
            # OTP is correct, proceed to reset password
            return render(request, 'driver_app/reset_password.html', {'email': email})
        else:
            # OTP mismatch
            return render(request, 'driver_app/verify_otp.html', {
                'error': 'Invalid OTP. Please try again.',
                'email': email
            })

    return redirect('driver_app:forgot_password')  # Redirect to forgot password page if not POST




def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # This will now be passed properly from the previous form
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'driver_app/reset_password.html', {'error': 'Passwords do not match.', 'email': email})

        try:
            driver = Driver.objects.get(email=email)
            driver.set_password(password)
            driver.save()
            # Redirect to login after password reset
            return redirect('driver_app:driver_login')
        except Driver.DoesNotExist:
            return render(request, 'driver_app/reset_password.html', {'error': 'Invalid email.', 'email': email})


def driver_dashboard(request, driver_id):
    # Fetch the driver and associated bookings
    driver = Driver.objects.get(driver_id=driver_id)
    vans = Van.objects.filter(driver=driver)
    bookings = CustomBooking.objects.filter(van__in=vans)

    # Serialize the bookings into JSON format
    booking_data = serialize('json', bookings, fields=('full_name', 'pickup_datetime', 'pickup_address', 'dropoff_address', 'passenger_count', 'contact_number', 'email_address', 'round_trip', 'additional_notes'))

    # Pass the serialized booking data and driver to the template
    context = {
        'driver': driver,  # Ensure this is included in context
        'booking_data_json': booking_data
    }

    return render(request, 'driver_app/driverdashboard.html', context)



def driver_my_vans(request, driver_id):
    # Fetch the driver and their vans
    driver = get_object_or_404(Driver, driver_id=driver_id)
    vans = Van.objects.filter(driver=driver)
    
    context = {
        'driver': driver,
        'vans': vans,
    }
    
    return render(request, 'driver_app/drivermyvan.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Temporarily disable CSRF for testing purposes (remove this in production)
def update_availability(request, driver_id, van_id):
    if request.method == 'POST':
        # Parse the incoming JSON data
        try:
            data = json.loads(request.body)
            driver_id = data.get('driver_id')
            availability = data.get('availability')

            # Ensure that the availability is a boolean value
            if isinstance(availability, bool):
                # Get the van object
                van = Van.objects.get(id=van_id)
                # Update the van's availability
                van.availability = availability
                van.save()

                # Return a success response
                return JsonResponse({'status': 'success', 'availability': van.availability})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid availability value'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
