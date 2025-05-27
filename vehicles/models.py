from django.db import models
from django.contrib.auth.models import User

FUEL_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Petrol & LPG', 'Petrol & LPG'),
    ('Diesel', 'Diesel'),
    ('Hybrid', 'Hybrid'),
    ('Electric', 'Electric'),
]

TRANSMISSION_CHOICES = [
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    
class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    km = models.IntegerField()

    fuel_type = models.CharField(max_length=50, choices=[
        ('Gasoline', 'Gasoline'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('LPG', 'LPG'),
    ],
    default='Gasoline')
    transmission = models.CharField(max_length=20, default='Automatic')
    engine_power = models.IntegerField(default=100)
    sunroof = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default='Unknown')   
    location = models.CharField(max_length=100, default='Unknown')   
    is_for_rent = models.BooleanField(default=False)  # Satılık mı Kiralık mı
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return f"{self.brand} {self.model}"
    
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')