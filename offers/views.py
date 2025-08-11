# offers/views.py

from rest_framework import generics, permissions
from .models import Offer
from .serializers import OfferDetailSerializer

class OfferDetailView(generics.RetrieveAPIView):
    """
    View para buscar os detalhes de uma única oferta pelo seu slug.
    Acessível por qualquer pessoa (não precisa de login).
    """
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    # Diz ao Django para procurar a oferta pelo campo de texto 'slug'
    # em vez do seu ID numérico.
    lookup_field = 'slug'