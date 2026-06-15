from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from apps.core.models import BaseModel
from django.db import models
from django.utils import timezone


def check_mayor(value):
    today = timezone.localdate()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('You must be 18 or older to register.')


class Address(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.street_address}, {self.city} ({self.state})"

class Account(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(validators=[check_mayor])
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_organizer = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']




