# Generated by Django 5.1.2 on 2024-11-05 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_remove_van_package_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='file_upload',
            field=models.ImageField(default='N/A', upload_to='driver_images/'),
        ),
    ]
