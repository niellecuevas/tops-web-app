from django import forms
from .models import Booking

class Booking(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'passenger_count',
                  'contact_number', 'pickup_datetime', 'pickup_address', 'dropoff_address',
                  'additional_notes','round_trip']
    def __init__(self, *args, **kwargs):
        super(Booking, self).__init__(*args, **kwargs)
        # Set initial values to empty for pickup_address and drop_off_address
        self.fields['pickup_address'].initial = ''
        self.fields['dropoff_address'].initial = ''