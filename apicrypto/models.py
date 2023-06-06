from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)
    price_now = models.DecimalField(max_digits=11, decimal_places=2)
    changes = models.DecimalField(max_digits=11, decimal_places=2)


class Weather(models.Model):
    city = models.CharField(max_length=35)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
