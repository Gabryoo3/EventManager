
from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    path('list_tickets/', views.TicketListView.as_view(), name='list'),
    path('ticket/<uuid:pk>/', views.TicketDetailView.as_view(), name='detail'),
    path('ticket_purchase/', views.BuyTicket.as_view(), name='purchase'),
    path('<uuid:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket_delete')
]