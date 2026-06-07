from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.account.models import Address

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

class Event(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    description = models.TextField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=False, blank=False)
    location = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='events')
    seats = models.PositiveIntegerField(default=0)



