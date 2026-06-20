from django.shortcuts import render
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from apps.events.models import Event
from .models import Ticket
# Create your views here.

class BuyTicket(LoginRequiredMixin, View):
    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        tickets_sold = Ticket.objects.filter(event=event).count()
        if tickets_sold >= event.seats:
            messages.error(request, f'The event "{event.title}" is sold out. You cannot buy a ticket.')
            return redirect('/events:detail', pk=event.pk)

        ticket = Ticket.objects.create(
            event=event,
            buyer=request.user,
            price = event.price
        )
        messages.success(request, f'Purchase successful! Your ticket code is {ticket.ticket_code}. Redirecting to home page.')
        return redirect('/')
class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')
    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.buyer

class TicketDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.buyer

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    def get_queryset(self):
        return Ticket.objects.filter(buyer=self.request.user).select_related('event')




