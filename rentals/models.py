from django.db import models
from accounts.models import User


class Bicycle(models.Model):
    """Модель велосипеда"""

    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)


class Rental(models.Model):
    """Модель аренды велосипеда"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                               blank=True)
