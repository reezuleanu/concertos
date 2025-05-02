from django.db import models

# Create your models here.


class Device(models.Model):
    """Holds device info"""

    event_id: any = models.CharField(max_length=50)
    name: str = models.CharField(max_length=50)
    type: str = models.CharField(max_length=50)
    address: str = models.CharField(max_length=15)
    port: int = models.IntegerField()


class CustomVariable(models.Model):
    """Custom variable class"""

    event_id: int = models.IntegerField(default=0)
    user_id: int = models.IntegerField(default=None, null=True, blank=True)
    name: str = models.CharField(max_length=50)
    value: int = models.IntegerField(default=0)
