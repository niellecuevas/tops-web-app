# Generated by Django 5.1.2 on 2024-10-30 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_destination'),
        ('customer_app', '0013_remove_custombooking_van_custombooking_package_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombooking',
            name='van',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='admin_app.van'),
        ),
    ]