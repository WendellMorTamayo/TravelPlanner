from django.contrib import admin
from .models import Trip, Activity, Itinerary, Destination

# Register your models here.
admin.site.register(Trip)
admin.site.register(Destination)
admin.site.register(Itinerary)
admin.site.register(Activity)

