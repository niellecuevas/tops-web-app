# Generated by Django 5.1.1 on 2024-10-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]