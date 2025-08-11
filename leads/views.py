# leads/views.py

from rest_framework import generics, permissions
from .models import Lead
from .serializers import LeadCreateSerializer

class LeadCreateView(generics.CreateAPIView):
    """
    View para receber e criar uma nova Solicitação de Reserva (Lead).
    Acessível por qualquer pessoa.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadCreateSerializer
    permission_classes = [permissions.AllowAny] # Qualquer pessoa pode enviar uma solicitação