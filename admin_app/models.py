from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

class Driver(models.Model):
    DRIVER_ID_PREFIX = 'DRV'  # Prefix for the driver ID

    # Driver ID will be auto-generated with prefix and unique number
    id = models.AutoField(primary_key=True)
    driver_id = models.CharField(max_length=10, unique=True, editable=False)
    file_upload = models.ImageField(upload_to='driver_images/', blank=False, default='N/A')
    name = models.CharField(max_length=100)
    license = models.CharField(max_length=50, default='N/A')  # Default value set
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)  # Hashed password

    def save(self, *args, **kwargs):
        # Automatically generate the driver ID
        if not self.driver_id:
            count = Driver.objects.count() + 1
            self.driver_id = f"{self.DRIVER_ID_PREFIX}{count:04d}"  # DRV0001, DRV0002, etc.
        if not self.license:
            self.license = 'N/A'
        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


    def __str__(self):
        return f"{self.name} - {self.driver_id}"
    

class Van(models.Model):
    file_upload = models.ImageField(upload_to='vans/', blank=False)
    model = models.CharField(max_length=100)  # Ensure this line exists
    plate = models.CharField(max_length=100)
    seats = models.IntegerField()
    is_company_van = models.BooleanField(default=False)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    description = models.TextField( default='Not defined')
    engine = models.CharField(max_length=50,default='Not defined')
    transmission = models.CharField(max_length=50,default='Not defined')
    ac = models.CharField(max_length=50,default='Not defined')
    entertainment = models.CharField(max_length=50,default='Not defined')
    storage = models.TextField(default='Not defined')

    def __str__(self):
        return self.model
    
class VanGallery(models.Model):
    van = models.ForeignKey(Van, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='van_gallery/', blank=False)
    
class Destination(models.Model):
    file_upload = models.ImageField(upload_to='destination/', blank=False)
    destination1 = models.CharField(max_length=100)  # Ensure this line exists
    destination2 = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.0')

class DynamicPricing(models.Model):
    destination = models.CharField(max_length=255)
    date = models.DateField()
    forecasted_pax = models.IntegerField()
    dynamic_price = models.FloatField()