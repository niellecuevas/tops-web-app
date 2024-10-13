from django.shortcuts import render
from django.shortcuts import redirect
from .forms import Booking  # Import your form here

'''def bookvanform(request):
    if request.method == 'POST':
        form = Booking(request.POST, request.FILES)  # Include request.FILES if you're handling file uploads
        if form.is_valid():
            print("Form is valid")
            
            # Create a new instance of the Booking model but do not save it yet
            booking = form.save(commit=False)
            
            # Manually set boolean values based on the presence of checkboxes
            booking.with_infant = 'with_infant' in request.POST
            booking.with_pwd = 'with_pwd' in request.POST
            booking.with_senior = 'with_senior' in request.POST

            if not form.cleaned_data.get('pickup_address'):
                booking.pickup_address = 'Not Specified'
            if not form.cleaned_data.get('drop_off_address'):
                booking.drop_off_address = 'Not Specified'

            passenger_count = form.cleaned_data.get('passenger_count')
            booking.grand_total = passenger_count * 1000
            
            # Now save the booking instance
            booking.save()
            
            # Redirect to the success page
            return redirect('success')  # 'success' is the name of your URL pattern for success.html
        else:
            # If the form is not valid, it will render the form again with errors
            print(form.errors)
            print("Form is not valid")
            return render(request, 'customer_app/bookvanform.html', {'form': form})
    else:
        # Show empty form if it's a GET request
        form = Booking()
        return render(request, 'customer_app/bookvanform.html', {'form': form})
'''
from django.shortcuts import render

def bookvanform(request):
    if request.method == 'POST':
        # Retrieve data from the form
        full_name = request.POST.get('full_name')
        passenger_count = request.POST.get('passenger_count')
        with_infant = request.POST.get('with_infant', 'False')  # Default to 'False' if not checked
        with_pwd = request.POST.get('with_pwd', 'False')  # Default to 'False' if not checked
        with_senior = request.POST.get('with_senior', 'False')  # Default to 'False' if not checked
        contact_number = request.POST.get('contact_number')
        pickup_datetime = request.POST.get('pickup_datetime')
        pickup_address = request.POST.get('pickup_address')
        dropoff_address = request.POST.get('dropoff_address')
        additional_notes = request.POST.get('additional_notes')
        round_trip = request.POST.get('round_trip', 'False')  # Default to 'False' if not checked

        # Store data in the session
        request.session['full_name'] = full_name
        request.session['passenger_count'] = passenger_count
        request.session['with_infant'] = with_infant
        request.session['with_pwd'] = with_pwd
        request.session['with_senior'] = with_senior
        request.session['contact_number'] = contact_number
        request.session['pickup_datetime'] = pickup_datetime
        request.session['pickup_address'] = pickup_address
        request.session['dropoff_address'] = dropoff_address
        request.session['additional_notes'] = additional_notes
        request.session['round_trip'] = round_trip

        # Prepare the context for rendering the summary
        context = {
            'full_name': full_name,
            'passenger_count': passenger_count,
            'with_infant': with_infant,
            'with_pwd': with_pwd,
            'with_senior': with_senior,
            'contact_number': contact_number,
            'pickup_datetime': pickup_datetime,
            'pickup_address': pickup_address,
            'dropoff_address': dropoff_address,
            'additional_notes': additional_notes,
            'round_trip': round_trip,
        }

        return render(request, 'customer_app/payment_summary.html', context)

    # Prepopulate form fields if data exists in the session
    context = {
        'full_name': request.session.get('full_name', ''),
        'passenger_count': request.session.get('passenger_count', ''),
        'with_infant': request.session.get('with_infant', 'False'),
        'with_pwd': request.session.get('with_pwd', 'False'),
        'with_senior': request.session.get('with_senior', 'False'),
        'contact_number': request.session.get('contact_number', ''),
        'pickup_datetime': request.session.get('pickup_datetime', ''),
        'pickup_address': request.session.get('pickup_address', ''),
        'dropoff_address': request.session.get('dropoff_address', ''),
        'additional_notes': request.session.get('additional_notes', ''),
        'round_trip': request.session.get('round_trip', 'False'),
    }
    
    return render(request, 'customer_app/bookvanform.html', context)




def customerhomepage(request):
    return render(request, 'customer_app/customerhomepage.html') 

def cstmrbookingdetails(request):
    return render(request, 'customer_app/cstmrbookingdetails.html') 

def success(request):
    # Optionally, you can pass more context if needed
    return render(request, 'customer_app/success.html')


def customer_homepage2(request):
    came_from_payment = request.GET.get('came_from_payment', 'false')  # Defaults to 'false'
    
    context = {
        'came_from_payment': came_from_payment,
        'full_name': request.session.get('full_name', ''),
        'passenger_count': request.session.get('passenger_count', ''),
        'with_infant': request.session.get('with_infant', 'False'),
        'with_pwd': request.session.get('with_pwd', 'False'),
        'with_senior': request.session.get('with_senior', 'False'),
        'contact_number': request.session.get('contact_number', ''),
        'pickup_datetime': request.session.get('pickup_datetime', ''),
        'pickup_address': request.session.get('pickup_address', ''),
        'dropoff_address': request.session.get('dropoff_address', ''),
        'additional_notes': request.session.get('additional_notes', ''),
        'round_trip': request.session.get('round_trip', 'False'),

    }

    # Check if the user came from the payment page
    if 'came_from_payment' not in request.GET:
        # Clear the session data only when NOT coming from the payment page
        keys_to_clear = [
            'full_name', 'passenger_count', 'with_infant', 'with_pwd', 
            'with_senior', 'contact_number', 'pickup_datetime', 
            'pickup_address', 'dropoff_address', 'additional_notes', 'round_trip'
        ]
        
        # Clear each key from the session
        for key in keys_to_clear:
            if key in request.session:
                del request.session[key]
    return render(request, 'customer_app/customerhomepage2.html', context)  # Use the correct path


def bookvan(request):
    return render(request, 'customer_app/bookvan.html')

def footer(request):
    return render(request, 'customer_app/footer.html')

def payment_summary(request):
    return render(request, 'customer_app/payment_summary.html')





