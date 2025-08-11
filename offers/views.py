# offers/views.py

from rest_framework import generics, permissions
from .models import Offer
from .serializers import OfferDetailSerializer

class OfferDetailView(generics.RetrieveAPIView):
    """
    View para buscar os detalhes de uma única oferta pelo seu slug.
    """
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

# --- NOVA VIEW ADICIONADA AQUI ---
class ServiceOffersListView(generics.ListAPIView):
    """
    View para listar TODAS as ofertas ativas de um serviço específico.
    """
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Pega o 'slug' do serviço a partir da URL
        service_slug = self.kwargs.get('service_slug')
        # Filtra e retorna apenas as ofertas que são daquele serviço E que estão ativas.
        # A regra 'show_on_landing_page' é ignorada aqui, como você pediu.
        return Offer.objects.filter(service__slug=service_slug, is_active=True)