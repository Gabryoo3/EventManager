from django.contrib.auth.models import AbstractUser
from apps.core.models import BaseModel
from django.db import models


class Address(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

class Account(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.IntegerField()
    is_organizer = models.BooleanField(default=False)


