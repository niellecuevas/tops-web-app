# Generated by Django 5.1.1 on 2024-10-09 13:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('passenger_count', models.PositiveIntegerField()),
                ('with_infant', models.BooleanField(default=False)),
                ('with_pwd', models.BooleanField(default=False)),
                ('with_senior', models.BooleanField(default=False)),
                ('contact_number', models.CharField(max_length=15)),
                ('pickup_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
