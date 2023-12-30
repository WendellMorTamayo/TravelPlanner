from django.db import models
from user.models import User


# Create your models here.
class Destination(models.Model):
    destination_id = models.AutoField(primary_key=True)
    destination_name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=2000, null=False)
    location = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.destination_name


class Trip(models.Model):
    trip_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=1000, null=False)
    start_date = models.DateField()

    def __str__(self):
        return self.title


class Activity(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=2000)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    location = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    itinerary_id = models.BigAutoField(primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    dates = models.DateField(auto_now=True)
    notes = models.CharField(max_length=100)

    def __str__(self):
        return self.itinerary_id
