from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(TimeStampModel):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Favorite(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(null=True, blank=True)
    original_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}, {self.original_url}"
