from django import forms
from .models import Booking, CustomBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'full_name', 'contact_number', 'pickup_datetime', 
            'passenger_count', 'additional_notes', 'round_trip', 'payment_mode'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_datetime': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'passenger_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'round_trip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
        }


class CustomBooking(forms.ModelForm):
    class Meta:
        model = CustomBooking
        fields = ['full_name', 'passenger_count',
                  'contact_number', 'pickup_datetime', 'pickup_address', 'dropoff_address',
                  'additional_notes','round_trip']
    def __init__(self, *args, **kwargs):
        super(CustomBooking, self).__init__(*args, **kwargs)
        # Set initial values to empty for pickup_address and drop_off_address
        self.fields['pickup_address'].initial = ''
        self.fields['dropoff_address'].initial = ''