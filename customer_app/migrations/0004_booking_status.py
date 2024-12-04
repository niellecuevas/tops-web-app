# Generated by Django 5.1.2 on 2024-12-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0003_booking_final_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending', max_length=10),
        ),
    ]
