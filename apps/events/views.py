from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, View, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from apps.account.models import Address
from apps.account.forms import AddressCreationForm, AddressUpdateForm
from .models import Event
from .forms import EventForm
# Create your views here.

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'organizer').filter(date__gte=timezone.localdate()).order_by('date')
        query_title = self.request.GET.get('title')
        category_name = self.request.GET.get('category')
        organizer_name = self.request.GET.get('organizer')
        remaining_seats = self.request.GET.get('remaining_seats')
        if query_title:
            queryset = queryset.filter(title__icontains=query_title)
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        if organizer_name:
            queryset = queryset.filter(organizer__stagename__icontains=organizer_name)
        if remaining_seats:
            queryset = queryset.filter(remaining_seats__gt=0)
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, View, SuccessMessageMixin):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EventForm
    success_url = reverse_lazy('events:organizer_events_list')
    success_message = 'Evento creato con successo!'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'address_form' : AddressCreationForm()
        })
    def post(self, request, *args, **kwargs):
        event_form = self.form_class(data=request.POST, files=request.FILES)
        address_form = AddressCreationForm(data=request.POST)
        if event_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            event = event_form.save(commit=False)
            event.organizer = self.request.user
            event.location = address
            event.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'form': event_form,
                'address_form': address_form
            })

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Event
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')
    success_message = 'Evento modificato con successo!'
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        address = event.location
        return render(request, self.template_name, {
            'form': EventForm(instance=event),
            'address_form' : AddressUpdateForm(instance=address)
        })
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        address = event.location
        eventForm = EventForm(data=request.POST, files=request.FILES, instance=event)
        addressForm = AddressUpdateForm(data=request.POST, instance=address)
        if eventForm.is_valid() and addressForm.is_valid():
            save_address=addressForm.save()
            eventForm.save(commit=False)
            event.location = save_address
            eventForm.save()
            messages.success(request, self.success_message)
            return redirect('events:organizer_events_list')
        return render(request, self.template_name, {
            'form' : EventForm(instance=event),
            'address_form' : AddressUpdateForm(request.POST),
        })
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs.get('pk'))
        return self.request.user == event.organizer

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:organizer_events_list')
    success_message = 'Evento eliminato con successo!'
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class HomepageCarouselView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'upcoming_events'
    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now()).prefetch_related('event_tickets').order_by('-date')[:7]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selling_out_events'] = Event.objects.filter(
            date__gte=timezone.localdate()
        ).annotate(
            sold_tickets=Count('event_tickets')
        ).annotate(
            tickets_remaining=F('seats') - F('sold_tickets')
        ).filter(
            tickets_remaining__gt=0,
            tickets_remaining__lte=15
        ).order_by('tickets_remaining')[:3]
        return context

class EventAttendeeListView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event
    template_name = 'events/event_attendees.html'
    context_object_name = 'event_attendees'
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.get_object().tickets.all().select_related('buyer').order_by('created_at')
        return context

class OrganizerEventsListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/organizer_list.html'
    context_object_name = 'organizer_events'
    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).order_by('-date')