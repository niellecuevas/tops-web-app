from django.db import models

class Driver(models.Model):
    DRIVER_ID_PREFIX = 'DRV'  # Prefix for the driver ID

    # Driver ID will be auto-generated with prefix and unique number
    id = models.AutoField(primary_key=True)
    driver_id = models.CharField(max_length=10, unique=True, editable=False)
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
        van_id = models.AutoField(primary_key=True)  # Unique identifier for the van
        model = models.CharField(max_length=100)      # Van model
        plate_number = models.CharField(max_length=20)  # Plate number
        capacity = models.IntegerField()               # Capacity of the van
        status = models.CharField(max_length=50, default='available')  # Status (e.g., available, unavailable)

    def __str__(self):
        return f"{self.model} - {self.plate_number}"
    
