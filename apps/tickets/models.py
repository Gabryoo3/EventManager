from django.db import models
from apps.account.models import Account
from apps.core.models import BaseModel
from apps.events.models import Event
import uuid
# Create your models here.

class Ticket(BaseModel):
    buyer = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='tickets')
    #for know when the ticket is purchased, use created_at of the base model
    price = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events')
    ticket_code = models.CharField(max_length=100, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.id} - {self.buyer.username} for {self.event.title}"


