# Generated by Django 5.1.1 on 2024-10-12 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0007_booking_grand_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='driver_van',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='grand_total',
        ),
    ]
