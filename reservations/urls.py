# reservations/urls.py

from django.urls import path
from .views import MyReservationsListView, CreateReservationView

urlpatterns = [
    path('my-reservations/', MyReservationsListView.as_view(), name='my_reservations'),
    # --- NOVA ROTA PARA CRIAR A RESERVA ---
    path('create/', CreateReservationView.as_view(), name='create_reservation'),
]