# reservations/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer, ReservationDocumentUploadSerializer, ReservationForReviewSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
import string

class MyReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(client=self.request.user)

class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
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

class ReservationsForReviewView(generics.ListAPIView):
    serializer_class = ReservationForReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(client=self.request.user, status='COMPLETED')
    
    # reservations/views.py

from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer, ReservationDocumentUploadSerializer, ReservationForReviewSerializer # Adicionado
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
import string

# ... (views existentes)

# --- NOVA VIEW PARA LISTAR RESERVAS CONCLUÍDAS ---
class ReservationsForReviewView(generics.ListAPIView):
    serializer_class = ReservationForReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as reservas do utilizador logado com o status 'Concluída'
        return Reservation.objects.filter(client=self.request.user, status='COMPLETED')