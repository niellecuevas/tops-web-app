from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license']

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        # Setting default values
        self.fields['license'].initial = ''  # Set initial to empty

from .models import Van
class VanForm(forms.ModelForm):
    class Meta:
        model = Van
        fields = ['file_upload', 'model', 'plate', 'seats', 'is_company_van', 'driver']

        def clean_image(self):
            file_upload = self.cleaned_data.get('image')
            if file_upload:
                if not file_upload.name.endswith(('.png', '.jpg', '.jpeg')):
                    raise forms.ValidationError("Only image files are allowed (PNG, JPG, JPEG).")
            return file_upload

        widgets = {
            'driver': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(VanForm, self).__init__(*args, **kwargs)
        # Set initial values to empty for van_model and plate_number
        self.fields['model'].initial = ''  # Set the initial value to empty
        self.fields['plate'].initial = ''  # Set the initial value to empty