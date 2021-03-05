# Register your models here.
from django.contrib import admin

from picture.models import Location, Favorite

admin.site.register(Location)
admin.site.register(Favorite)
