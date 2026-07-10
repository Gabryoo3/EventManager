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

    context_object_name = 'buy_ticket'
    def post(self, request, *args, **kwargs):
        print(request.POST)
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        quantity = int(request.POST.get('quantity',1))
        tickets_sold = Ticket.objects.filter(event=event).count()
        if tickets_sold + quantity > event.seats:
            messages.error(request, f"L'evento '{event.title}'ha meno biglietti di quanti chiesti.")
            return redirect('events:event_detail', pk=event.pk)
        tickets_created=[]
        for _ in range(quantity):
            ticket = Ticket.objects.create(
                event=event,
                buyer=request.user,
                price = event.price
            )
            tickets_created.append(ticket)
        messages.success(request, f'Acquisto completato! Ritorno alla lista eventi')
        return redirect('events:event_list')

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets:list')
    success_message = 'Biglietto eliminato con successo!'
    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.buyer
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

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
        return Ticket.objects.filter(buyer=self.request.user).select_related('event').order_by('event', 'created_at')




