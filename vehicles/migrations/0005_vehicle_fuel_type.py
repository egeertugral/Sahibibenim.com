# Generated by Django 5.2.1 on 2025-05-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0004_vehicleimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(choices=[('Gasoline', 'Gasoline'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid'), ('LPG', 'LPG')], default='Gasoline', max_length=50),
        ),
    ]
