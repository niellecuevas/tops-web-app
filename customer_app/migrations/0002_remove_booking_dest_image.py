# Generated by Django 5.1.2 on 2024-12-01 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='dest_image',
        ),
    ]
