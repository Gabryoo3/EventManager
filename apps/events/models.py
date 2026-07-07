from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.account.models import Address
from django.utils import timezone
from PIL import Image as PilImage, ImageOps


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name


def check_date(value):
    today = timezone.localdate()
    if value <= today:
        raise ValidationError("Non puoi creare un evento prima della data corrente!")


class Event(BaseModel):
    title = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    description = models.TextField(blank=True)
    date = models.DateField(format('%d/%m/%Y'), validators=[check_date])
    time = models.TimeField(format('%H:%M'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='events') #for many-to-one
    # one category can have many events but an event has only one category
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    location = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='events')
    seats = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            pil_img = PilImage.open(self.image.path)
            pil_img = ImageOps.fit(pil_img, (250,400), PilImage.Resampling.LANCZOS)
            pil_img.save(self.image.path)
    @property
    def remaining_seats(self):
        from apps.tickets.models import Ticket
        tickets_sold = self.event_tickets.count()
        return max(0,self.seats - tickets_sold)



