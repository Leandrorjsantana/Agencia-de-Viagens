# offers/views.py
from rest_framework import generics, permissions
from django.db.models import Q
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

class ServiceOffersListView(generics.ListAPIView):
    """
    View para listar todas as ofertas de um serviço, com filtros de busca.
    """
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        service_slug = self.kwargs.get('service_slug')
        
        if service_slug == 'todos':
            queryset = Offer.objects.filter(is_active=True)
        else:
            queryset = Offer.objects.filter(service__slug=service_slug, is_active=True)
        
        # Filtros da busca (se existirem na URL)
        query_params = self.request.query_params
        destination = query_params.get('destination', None)
        
        if destination:
            queryset = queryset.filter(
                Q(destination_city__icontains=destination) |
                Q(title__icontains=destination) |
                Q(subtitle__icontains=destination)
            )
        
        return queryset

class OfferForAdminView(generics.RetrieveAPIView):
    """
    View segura para o painel de admin buscar detalhes de uma oferta.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer # Pode ser um serializer mais simples
    permission_classes = [permissions.IsAdminUser]
