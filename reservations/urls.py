# reservations/urls.py

from django.urls import path
from .views import MyReservationsListView

urlpatterns = [
    # O endereço será: /api/v1/reservations/my-reservations/
    path('my-reservations/', MyReservationsListView.as_view(), name='my_reservations'),
]