# offers/views.py

from rest_framework import generics, permissions
from django.db.models import Q
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
        
        if service_slug == 'todos':
            queryset = Offer.objects.filter(is_active=True)
        else:
            queryset = Offer.objects.filter(service__slug=service_slug, is_active=True)

        query_params = self.request.query_params
        destination = query_params.get('destination', None)
        
        if destination:
            # CORREÇÃO: A busca agora é precisa e procura no novo campo 'destination_city',
            # mas também mantém a busca genérica nos outros campos para flexibilidade.
            queryset = queryset.filter(
                Q(destination_city__icontains=destination) |
                Q(title__icontains=destination) |
                Q(subtitle__icontains=destination)
            )
        
        return queryset