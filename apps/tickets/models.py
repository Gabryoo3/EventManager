from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.core.models import BaseModel
from apps.account.models import Account
from apps.events.models import Event
# Create your models here.

class Ticket(BaseModel):
    buyer = models.ForeignKey(Account, on_delete=models.PROTECT,null=False, blank=False)
    seat = models.PositiveIntegerField(default=0, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    purchaseDate = models.DateField(null=False, blank=False)
    price = models.PositiveIntegerField(default=0, null=False, blank=False)
    event = models.OneToOneField(Event, on_delete=models.PROTECT,null=False, blank=False)
