# reservations/urls.py

from django.urls import path
from .views import MyReservationsListView, DocumentUploadView

urlpatterns = [
    # Rota para listar as reservas
    path('my-reservations/', MyReservationsListView.as_view(), name='my_reservations'),

    # --- NOVA ROTA PARA O UPLOAD ---
    # O endereço será: /api/v1/reservations/<id_da_reserva>/upload-document/
    path('<int:reservation_id>/upload-document/', DocumentUploadView.as_view(), name='upload_document'),
]