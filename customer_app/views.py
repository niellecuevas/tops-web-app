from django.shortcuts import render, get_object_or_404
from admin_app.models import Van
from admin_app.models import Destination
from django.shortcuts import redirect
from .forms import Booking  # Import your form here

from django.shortcuts import render

def bookvanform(request):
    if request.method == 'POST':
        # Retrieve data from the form
        full_name = request.POST.get('full_name')
        passenger_count = request.POST.get('passenger_count')
        contact_number = request.POST.get('contact_number')
        pickup_datetime = request.POST.get('pickup_datetime')
        pickup_address = request.POST.get('pickup_address')
        dropoff_address = request.POST.get('dropoff_address')
        additional_notes = request.POST.get('additional_notes')
        round_trip = request.POST.get('round_trip') == 'on'  # This will be True if checked, False otherwise
        package_price  = request.POST.get('package_price')

        # Store data in the session
        request.session['full_name'] = full_name
        request.session['passenger_count'] = passenger_count
        request.session['contact_number'] = contact_number
        request.session['pickup_datetime'] = pickup_datetime
        request.session['pickup_address'] = pickup_address
        request.session['dropoff_address'] = dropoff_address
        request.session['additional_notes'] = additional_notes
        request.session['round_trip'] = round_trip
        request.session['package_price'] = package_price


        # Retrieve and calculate package price
        passenger_count = int(passenger_count) if passenger_count else 0
        package_price = int(request.POST.get('package_price', 0))
        
        # Ensure price is calculated even if JavaScript fails
        if not package_price:
            package_price = passenger_count * 100


        # Prepare the context for rendering the summary
        context = {
            'full_name': full_name,
            'passenger_count': passenger_count,
            'contact_number': contact_number,
            'pickup_datetime': pickup_datetime,
            'pickup_address': pickup_address,
            'dropoff_address': dropoff_address,
            'additional_notes': additional_notes,
            'round_trip': round_trip,
            'package_price': package_price,
        }

        return render(request, 'customer_app/payment_summary_custom.html', context)

    # Prepopulate form fields if data exists in the session
    context = {
        'full_name': request.session.get('full_name', ''),
        'passenger_count': request.session.get('passenger_count', ''),
        'contact_number': request.session.get('contact_number', ''),
        'pickup_datetime': request.session.get('pickup_datetime', ''),
        'pickup_address': request.session.get('pickup_address', ''),
        'dropoff_address': request.session.get('dropoff_address', ''),
        'additional_notes': request.session.get('additional_notes', ''),
        'round_trip': request.session.get('round_trip', 'False'),
        'package_price': request.session.get('package_price', ''),
    }
    
    return render(request, 'customer_app/bookvanform.html', context)


def bookdestination(request):
    if request.method == 'POST':
        # Retrieve data from the form
        full_name = request.POST.get('full_name')
        passenger_count = request.POST.get('passenger_count')
        contact_number = request.POST.get('contact_number')
        pickup_datetime = request.POST.get('pickup_datetime')
        additional_notes = request.POST.get('additional_notes')
        round_trip = request.POST.get('round_trip') == 'on'  # This will be True if checked, False otherwise

        # Store data in the session
        request.session['full_name'] = full_name
        request.session['passenger_count'] = passenger_count
        request.session['contact_number'] = contact_number
        request.session['pickup_datetime'] = pickup_datetime
        request.session['additional_notes'] = additional_notes
        request.session['round_trip'] = round_trip

        # Prepare the context for rendering the summary
        context = {
            'full_name': full_name,
            'passenger_count': passenger_count,
            'contact_number': contact_number,
            'pickup_datetime': pickup_datetime,
            'additional_notes': additional_notes,
            'round_trip': round_trip,
        }

        return render(request, 'customer_app/payment_summary.html', context)

    # Prepopulate form fields if data exists in the session
    context = {
        'full_name': request.session.get('full_name', ''),
        'passenger_count': request.session.get('passenger_count', ''),
        'contact_number': request.session.get('contact_number', ''),
        'dropoff_address': request.session.get('dropoff_address', ''),
        'additional_notes': request.session.get('additional_notes', ''),
        'round_trip': request.session.get('round_trip', 'False'),
    }
    
    return render(request, 'customer_app/bookdestination.html', context)




def customerhomepage(request):
    return render(request, 'customer_app/customerhomepage.html') 

def cstmrbookingdetails(request):
    return render(request, 'customer_app/cstmrbookingdetails.html') 

def success(request):
    # Optionally, you can pass more context if needed
    return render(request, 'customer_app/success.html')


def customer_homepage2(request):
    came_from_payment = request.GET.get('came_from_payment', 'false')  # Defaults to 'false'
    # Fetch the van with ID 23
    van = get_object_or_404(Van, id=1)
    van2 = get_object_or_404(Van, id=2)
    dest1 = get_object_or_404(Destination, id=1)
    dest2 = get_object_or_404(Destination, id=2)
    dest3 = get_object_or_404(Destination, id=3)
    dest5 = get_object_or_404(Destination, id=5)
    
    context = {
        'came_from_payment': came_from_payment,
        'full_name': request.session.get('full_name', ''),
        'passenger_count': request.session.get('passenger_count', ''),
        'contact_number': request.session.get('contact_number', ''),
        'pickup_datetime': request.session.get('pickup_datetime', ''),
        'pickup_address': request.session.get('pickup_address', ''),
        'dropoff_address': request.session.get('dropoff_address', ''),
        'additional_notes': request.session.get('additional_notes', ''),
        'round_trip': request.session.get('round_trip', 'False'),
        'van': van,  # Pass the van with ID 23 to the context
        'van2': van2,
        'dest1': dest1,
        'dest2': dest2,
        'dest3': dest3,
        'dest5': dest5,

    }

    # Check if the user came from the payment page
    if 'came_from_payment' not in request.GET:
        # Clear the session data only when NOT coming from the payment page
        keys_to_clear = [
            'full_name', 'passenger_count', 'contact_number', 'pickup_datetime', 
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
    return render(request, 'payment_summary.html')

def payment_summary_custom(request):
    return render(request, 'payment_summary_custom.html')





