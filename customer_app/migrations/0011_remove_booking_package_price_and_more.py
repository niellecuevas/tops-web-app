# Generated by Django 5.1.2 on 2024-10-29 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0010_booking_package_price_booking_payment_mode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='package_price',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='total_amount',
        ),
    ]
