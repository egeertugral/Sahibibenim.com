from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VehicleImage, Vehicle

@receiver(post_save, sender=VehicleImage)
def set_main_vehicle_image(sender, instance, created, **kwargs):
    if created and instance.vehicle.image is None:
        instance.vehicle.image = instance.image
        instance.vehicle.save()
