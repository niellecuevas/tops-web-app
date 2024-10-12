from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license', 'van_model', 'plate_number']

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        # Setting default values
        self.fields['license'].initial = ''  # Set initial to empty
        self.fields['van_model'].initial = ''
        self.fields['plate_number'].initial = ''