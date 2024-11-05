from django.db import models

class Driver(models.Model):
    DRIVER_ID_PREFIX = 'DRV'  # Prefix for the driver ID

    # Driver ID will be auto-generated with prefix and unique number
    id = models.AutoField(primary_key=True)
    driver_id = models.CharField(max_length=10, unique=True, editable=False)
    file_upload = models.ImageField(upload_to='driver_images/', blank=False, default='N/A')
    name = models.CharField(max_length=100)
    license = models.CharField(max_length=50, default='N/A')  # Default value set

    def save(self, *args, **kwargs):
        # Automatically generate the driver ID
        if not self.driver_id:
            count = Driver.objects.count() + 1
            self.driver_id = f"{self.DRIVER_ID_PREFIX}{count:04d}"  # DRV0001, DRV0002, etc.
        if not self.license:
            self.license = 'N/A'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.driver_id}"
    

class Van(models.Model):
    file_upload = models.ImageField(upload_to='vans/', blank=False)
    model = models.CharField(max_length=100)  # Ensure this line exists
    plate = models.CharField(max_length=100)
    seats = models.IntegerField()
    is_company_van = models.BooleanField(default=False)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)

    def __str__(self):
        return self.model
    
class Destination(models.Model):
    file_upload = models.ImageField(upload_to='destination/', blank=False)
    destination1 = models.CharField(max_length=100)  # Ensure this line exists
    destination2 = models.CharField(max_length=100)
    transportationfee = models.DecimalField(max_digits=10, decimal_places=2, default='0.0')