# favorites/models.py
from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vehicle')

    def __str__(self):
        return f"{self.user.username} favorited {self.vehicle}"
