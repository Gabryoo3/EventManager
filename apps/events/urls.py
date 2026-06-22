from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.HomepageCarouselView.as_view(), name='home'),
    path('explore/', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('list_organizer/', views.EventOrganizedView.as_view(), name='event_organizer'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]