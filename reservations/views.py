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
    
    # reservations/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer, ReservationDocumentUploadSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyReservationsListView(generics.ListAPIView):
    # ... (código existente)
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(client=self.request.user)

# --- NOVA VIEW PARA O UPLOAD DE DOCUMENTOS ---
class DocumentUploadView(generics.CreateAPIView):
    serializer_class = ReservationDocumentUploadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Pega o ID da reserva da URL
        reservation_id = self.kwargs.get('reservation_id')
        try:
            # Verifica se a reserva existe E se pertence ao usuário logado
            reservation = Reservation.objects.get(id=reservation_id, client=request.user)
        except Reservation.DoesNotExist:
            return Response({'detail': 'Reserva não encontrada ou não pertence a você.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Salva o documento, associando à reserva e marcando como 'CLIENT'
        serializer.save(reservation=reservation, uploaded_by='CLIENT')

        return Response(serializer.data, status=status.HTTP_201_CREATED)