from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    email = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=11, null=False)
    balance = models.FloatField(default=0)

    def __str__(self):
        if self.user_id is None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return f'{self.firstname} {self.lastname}'

