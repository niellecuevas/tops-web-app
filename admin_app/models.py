from django.db import models

class Driver(models.Model):
    DRIVER_ID_PREFIX = 'DRV'  # Prefix for the driver ID

    # Driver ID will be auto-generated with prefix and unique number
    driver_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    license = models.CharField(max_length=50, default='N/A')  # Default value set
    van_model = models.CharField(max_length=100, default='N/A')  # Default value set
    plate_number = models.CharField(max_length=20, default='N/A')

    def save(self, *args, **kwargs):
        # Automatically generate the driver ID
        if not self.driver_id:
            count = Driver.objects.count() + 1
            self.driver_id = f"{self.DRIVER_ID_PREFIX}{count:04d}"  # DRV0001, DRV0002, etc.
        if not self.license:
            self.license = 'N/A'
        if not self.van_model:
            self.van_model = 'N/A'
        if not self.plate_number:
            self.plate_number = 'N/A'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.driver_id}"
    
