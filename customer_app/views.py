from django.shortcuts import render
from django.shortcuts import redirect
from .forms import Booking  # Import your form here

def customer_form_view(request):
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
            return render(request, 'customer_app/customerform.html', {'form': form})
    else:
        # Show empty form if it's a GET request
        form = Booking()
        return render(request, 'customer_app/customerform.html', {'form': form})



def customerhomepage(request):
    return render(request, 'customer_app/customerhomepage.html') 

def cstmrbookingdetails(request):
    return render(request, 'customer_app/cstmrbookingdetails.html') 

def success(request):
    # Optionally, you can pass more context if needed
    return render(request, 'customer_app/success.html')


