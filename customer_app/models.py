from django.db import models
from django.utils import timezone
from admin_app.models import Van, Destination
class Booking(models.Model):
    full_name = models.CharField(max_length=255)
    passenger_count = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    additional_notes = models.TextField(blank=True, null=True)
    round_trip = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=255, default='Not Specified')
    van = models.ForeignKey(Van, on_delete=models.CASCADE, default='0')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, default='0')
    payment_mode = models.CharField(max_length=50)
    proof_of_payment = models.FileField(upload_to='payments/', blank=True, null=True)

    #def __str__(self):
    #    return f'Booking: {self.full_name} on {self.pickup_datetime}'

class CustomBooking(models.Model):
    full_name = models.CharField(max_length=255)
    passenger_count = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    pickup_address = models.CharField(max_length=255, default='Not Specified')
    dropoff_address = models.CharField(max_length=255, default='Not Specified')
    additional_notes = models.TextField(blank=True, null=True)
    round_trip = models.BooleanField(default=False)
    package_price = models.CharField(max_length=255, default='Not Specified')
    van = models.ForeignKey(Van, on_delete=models.CASCADE, default='0')
    payment_mode = models.CharField(max_length=50)
    proof_of_payment = models.FileField(upload_to='payments/', blank=True, null=True)


