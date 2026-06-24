from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm
# Create your views here.

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'event'
    def get_queryset(self):
        queryset = super().get_queryset().filter(date__gte=timezone.localdate()).order_by('date')
        query_title = self.request.GET.get('title')
        category_name = self.request.GET.get('category')
        if query_title:
            queryset = queryset.filter(title__icontains=query_title)
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event_list')
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form) #makes the user that created the event the owner

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

class HomepageCarouselView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'upcoming_events'
    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now()).order_by('-date')[:7]

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