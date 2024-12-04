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
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, default='1')
    payment_mode = models.CharField(max_length=50)
    proof_of_payment = models.FileField(upload_to='payments/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'),],
        default='Pending'  # Default status is "Pending"
    )

    # New fields for destination information
    destination1 = models.CharField(max_length=255, blank=True, null=True)
    destination2 = models.CharField(max_length=255, blank=True, null=True)
    transportation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class CustomBooking(models.Model):
    full_name = models.CharField(max_length=255)
    passenger_count = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=254, default='Not Specified')
    pickup_datetime = models.DateTimeField(default=timezone.now)
    pickup_address = models.CharField(max_length=255, default='Not Specified')
    dropoff_address = models.CharField(max_length=255, default='Not Specified')
    additional_notes = models.TextField(blank=True, null=True)
    round_trip = models.BooleanField(default=False)
    van = models.ForeignKey(Van, on_delete=models.CASCADE, default='0')
    custom_status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'),('Cancelled', 'Cancelled'),],
        default='Pending'  # Default status is "Pending"
    )

