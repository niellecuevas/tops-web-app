from django import forms
from .models import Booking

class Booking(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'passenger_count', 'with_infant', 'with_pwd', 'with_senior',
                  'contact_number', 'pickup_datetime', 'pickup_address', 'dropoff_address',
                  'driver_van']
