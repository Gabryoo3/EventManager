from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.HomepageCarouselView.as_view(), name='home'),
    path('explore/', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:id>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:id>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:id>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('managedEvents/', views.OrganizerEventsListView.as_view(), name='organizer_events_list')
]