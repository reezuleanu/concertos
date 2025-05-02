from django.db import models
from cities_light.models import City, Country

# Create your models here.


class Event(models.Model):

    name: str = models.CharField(max_length=50)
    owner_id: int = models.IntegerField(default=0)
    description: str = models.TextField(max_length=255)
    country: str = models.ForeignKey(Country, on_delete=models.CASCADE)
    city: str = models.ForeignKey(City, on_delete=models.CASCADE)
    # participants: list[int] = models.ArrayField()
    # participants.append(owner_id)
