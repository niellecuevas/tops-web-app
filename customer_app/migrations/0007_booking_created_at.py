# Generated by Django 5.1.2 on 2025-01-02 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0006_alter_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
