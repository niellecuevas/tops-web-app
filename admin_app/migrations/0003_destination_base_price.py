# Generated by Django 5.1.2 on 2024-11-30 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_dynamicpricing'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10),
        ),
    ]
