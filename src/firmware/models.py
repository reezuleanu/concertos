from django.db import models


# Create your models here.
class Firmware(models.Model):

    name: str = models.CharField(max_length=64)
    version: str = models.CharField(max_length=10)
    description: str = models.TextField(max_length=256)
    path: str = models.CharField(max_length=64)
