# offers/views.py

from rest_framework import generics, permissions
from .models import Offer
from .serializers import OfferDetailSerializer

class OfferDetailView(generics.RetrieveAPIView):
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class ServiceOffersListView(generics.ListAPIView):
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        service_slug = self.kwargs.get('service_slug')
        
        # --- LÓGICA INTELIGENTE ADICIONADA AQUI ---
        # Se o slug for 'todos', retorna todas as ofertas ativas.
        if service_slug == 'todos':
            return Offer.objects.filter(is_active=True)
        
        # Caso contrário, continua a filtrar pelo serviço específico.
        return Offer.objects.filter(service__slug=service_slug, is_active=True)