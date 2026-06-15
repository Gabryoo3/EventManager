from django.contrib import admin
from apps.tickets.models import Ticket


# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'price', 'event', 'ticket_code', 'created_at')
    search_fields = ('buyer__username', 'event__title', 'ticket_code')
    list_filter = ('event', 'created_at')