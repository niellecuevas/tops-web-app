from django.db import models

class Driver(models.Model):
    DRIVER_ID_PREFIX = 'DRV'  # Prefix for the driver ID

    # Driver ID will be auto-generated with prefix and unique number
    driver_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Automatically generate the driver ID
        if not self.driver_id:
            count = Driver.objects.count() + 1
            self.driver_id = f"{self.DRIVER_ID_PREFIX}{count:04d}"  # DRV0001, DRV0002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.driver_id}"
