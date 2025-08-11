# reservations/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer, ReservationDocumentUploadSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
import string

class MyReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(client=self.request.user)

# --- VIEW QUE FALTAVA ADICIONADA AQUI ---
class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Gera um código de reserva aleatório
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Salva a reserva, associando-a ao cliente logado
        serializer.save(client=self.request.user, reservation_code=code)

class DocumentUploadView(generics.CreateAPIView):
    serializer_class = ReservationDocumentUploadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reservation_id = self.kwargs.get('reservation_id')
        try:
            reservation = Reservation.objects.get(id=reservation_id, client=self.request.user)
            serializer.save(reservation=reservation, uploaded_by='CLIENT')
        except Reservation.DoesNotExist:
            pass