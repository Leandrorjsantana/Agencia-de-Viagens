# reservations/urls.py

from django.urls import path
from .views import (
    MyReservationsListView, 
    CreateReservationView, 
    DocumentUploadView, 
    ReservationsForReviewView
)

urlpatterns = [
    # Rota para o cliente listar as suas próprias reservas
    # GET /api/v1/reservations/my-reservations/
    path('my-reservations/', MyReservationsListView.as_view(), name='my_reservations'),

    # Rota para o cliente criar uma nova reserva (a partir da página de detalhes da oferta)
    # POST /api/v1/reservations/create/
    path('create/', CreateReservationView.as_view(), name='create_reservation'),

    # Rota para o cliente fazer upload de um documento para uma reserva específica
    # POST /api/v1/reservations/1/upload-document/
    path('<int:reservation_id>/upload-document/', DocumentUploadView.as_view(), name='upload_document'),

    # Rota para buscar as reservas concluídas que podem ser avaliadas
    # GET /api/v1/reservations/for-review/
    path('for-review/', ReservationsForReviewView.as_view(), name='reservations_for_review'),
]
