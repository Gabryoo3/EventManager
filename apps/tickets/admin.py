from django.contrib import admin
from apps.tickets.models import Ticket


# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'price', 'event', 'ticket_code', 'created_at')
    fields = ('buyer', 'price', 'event')
    search_fields = ('buyer__username', 'event__title', 'ticket_code')
    list_filter = ('buyer', 'event', 'created_at')