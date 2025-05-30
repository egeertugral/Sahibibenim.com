# Generated by Django 5.2.1 on 2025-05-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='color',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine_power',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='location',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='sunroof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='transmission',
            field=models.CharField(default='Automatic', max_length=20),
        ),
    ]
