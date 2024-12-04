from django.shortcuts import render, get_object_or_404
from admin_app.models import Van, Driver
from admin_app.models import Destination
from django.shortcuts import redirect
from .forms import Booking  # Import your form here

from django.shortcuts import render

import xml.etree.ElementTree as ET
from django.templatetags.static import static

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


from .models import Booking
from django.http import HttpResponse

def save_booking(request):
    if request.method == 'POST':
        # Retrieve data from session (or from the request if you prefer)
        full_name = request.session.get('full_name')
        passenger_count = request.session.get('passenger_count')
        contact_number = request.session.get('contact_number')
        pickup_datetime = request.session.get('pickup_datetime')
        additional_notes = request.session.get('additional_notes')
        round_trip = request.session.get('round_trip', False)

        # Retrieve data from the form
        destination1 = request.POST.get("destination1")
        destination2 = request.POST.get("destination2")
        transportation_fee = request.POST.get("transportation_fee")
        final_fee = request.POST.get('final_fee')


        # Create and save the booking
        booking = Booking.objects.create(
            full_name=full_name,
            passenger_count=passenger_count,
            contact_number=contact_number,
            pickup_datetime=pickup_datetime,
            additional_notes=additional_notes,
            round_trip=round_trip,
            destination1=destination1,
            destination2=destination2,
            transportation_fee=transportation_fee,
            final_fee=final_fee
        )
        
        # Optionally, clear the session data
        request.session.flush()

        # Redirect or show a success message
        return redirect('success', booking_id=booking.id)  # Create a URL for a confirmation page if desired

    return HttpResponse("Invalid request method.", status=405)

def customisebook(request):
    van_type = request.GET.get('van_type', 'all')
    if van_type == 'company':
        vans = Van.objects.filter(is_company_van=True)
    elif van_type == 'driver_owned':
        vans = Van.objects.filter(is_company_van=False)
    else:
        vans = Van.objects.all()
        vans = Van.objects.filter(availability=True)
    return render(request, 'customer_app/customisebook.html', {'vans': vans})

def cstmrbookingdetails(request):
    return render(request, 'customer_app/cstmrbookingdetails.html') 

def search_custom_booking(request):
    custom_booking_details = None
    custom_booking_error = None

    if 'custom_booking_id' in request.GET:
        custom_booking_id = request.GET.get('custom_booking_id').strip()
        if custom_booking_id:
            try:
                custom_booking_details = CustomBooking.objects.select_related('van').get(id=custom_booking_id)
            except CustomBooking.DoesNotExist:
                custom_booking_error = f"No Custom Booking found with ID: {custom_booking_id}"

    return render(request,'customer_app/cstmrbookingdetails.html', {
        'custom_booking_details': custom_booking_details,
        'custom_booking_error': custom_booking_error,
    })

def search_standard_booking(request):
    standard_booking_details = None
    standard_booking_error = None

    if 'standard_booking_id' in request.GET:
        standard_booking_id = request.GET.get('standard_booking_id').strip()
        if standard_booking_id:
            try:
                standard_booking_details = Booking.objects.select_related('destination').get(id=standard_booking_id)
            except Booking.DoesNotExist:
                standard_booking_error = f"No Standard Booking found with ID: {standard_booking_id}"

    return render(request,'customer_app/cstmrbookingdetails.html', {
        'standard_booking_details': standard_booking_details,
        'standard_booking_error': standard_booking_error,
    })


def success(request, booking_id):
    try:
        # Retrieve the booking instance by its ID
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        booking = None  # Handle case where booking ID is invalid
    
    return render(request, 'customer_app/success.html', {'booking': booking})

from admin_app.models import DynamicPricing

def customer_homepage2(request):
    came_from_payment = request.GET.get('came_from_payment', 'false')  # Defaults to 'false'
    # Fetch the van with ID 23
    van = get_object_or_404(Van, id=1)
    van2 = get_object_or_404(Van, id=2)
    dest1 = get_object_or_404(Destination, id=1)
    dest2 = get_object_or_404(Destination, id=2)
    dest3 = get_object_or_404(Destination, id=3)

    # Query the dynamic pricing for the three destinations
    ppc_en_data = DynamicPricing.objects.filter(destination='PPC-EN').order_by('-date').first()  # Get the most recent data
    milan_data = DynamicPricing.objects.filter(destination='MILAN').order_by('-date').first()  # Get the most recent data
    frendz_data = DynamicPricing.objects.filter(destination='FRENDZ').order_by('-date').first()  # Get the most recent data

    
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
        'ppc_en_data': ppc_en_data,
        'milan_data': milan_data,
        'frendz_data': frendz_data
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
    destination_id = request.GET.get('destination_id')
    destination = get_object_or_404(Destination, id=destination_id)

    context = {
        'destination': destination
    }
    return render(request, 'payment_summary.html', context)


def terms_and_conditions(request):
    # Load the XML file
    tree = ET.parse(static('xml/terms.xml'))
    root = tree.getroot()

    # Parse XML into HTML
    terms = []
    for section in root.findall('section'):
        title = section.get('title')
        items = [item.text for item in section.findall('item')]
        content = section.find('content').text if section.find('content') is not None else ""
        notes = [note.text for note in section.findall('note')]
        terms.append({'title': title, 'content': content, 'items': items, 'notes': notes})

    return render(request, 'terms_modal.html', {'terms': terms})

def payment_summary_custom(request):
    return render(request, 'payment_summary_custom.html')

 

def vandetail(request, van_id):
    van = get_object_or_404(Van, id=van_id)
    driver = van.driver # Assuming each van has a related driver
    return render(request, 'customer_app/vandetail.html', {'van': van, 'driver': driver})

def base(request):
    return render(request, 'customer_app/base.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import CustomBooking, Van

def book_van(request, van_id):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        contact_number = request.POST['contact_number']
        email_address = request.POST['email']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        passenger_count = request.POST['passenger_count']  # Retrieve passenger count from the form
        pickup_address = request.POST['pickup_address']  # New pickup address
        dropoff_address = request.POST['dropoff_address']
        round_trip = 'round_trip' in request.POST
        additional_notes = request.POST.get('additional_notes', '')

        # Combine pickup_date and pickup_time into a single datetime object
        pickup_datetime = timezone.make_aware(
            timezone.datetime.combine(
                timezone.datetime.strptime(pickup_date, '%Y-%m-%d').date(),
                timezone.datetime.strptime(pickup_time, '%H:%M').time()
            )
        )

        # Get the van instance based on the van_id
        van = Van.objects.get(id=van_id)

        # Create a new booking instance
        booking = CustomBooking(
            full_name=full_name,
            contact_number=contact_number,
            email_address=email_address,
            pickup_datetime=pickup_datetime,
            passenger_count=passenger_count,  # Add passenger count to the booking instance
            pickup_address=pickup_address,  # Add pickup address
            dropoff_address=dropoff_address,  # Add dropoff address
            additional_notes=additional_notes,
            round_trip=round_trip,
            van=van
        )
        booking.save()  # Save the booking to the database

        # Redirect to a success page or driver dashboard
        return redirect('success')

    # If not a POST request, render the booking form (or redirect)
    van = Van.objects.get(id=van_id)
    return render(request, 'vandetail.html', {'van': van})









