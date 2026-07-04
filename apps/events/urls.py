from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.HomepageCarouselView.as_view(), name='home'),
    path('explore/', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<uuid:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<uuid:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<uuid:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('managedEvents/', views.OrganizerEventsListView.as_view(), name='organizer_events_list')
]