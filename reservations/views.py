# reservations/views.py

from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyReservationsListView(generics.ListAPIView):
    """
    View para um cliente listar suas próprias reservas.
    Acessível apenas por usuários autenticados.
    """
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # A lógica original e correta, que agora vai funcionar.
        return Reservation.objects.filter(client=self.request.user)