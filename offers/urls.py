# offers/urls.py

from django.urls import path
from .views import OfferDetailView, ServiceOffersListView

urlpatterns = [
    # Rota para os detalhes de uma oferta (já existia)
    path('<slug:slug>/', OfferDetailView.as_view(), name='offer_detail'),
    
    # --- NOVA ROTA ADICIONADA AQUI ---
    # O endereço será: /api/v1/offers/servico/<slug-do-servico>/
    path('servico/<slug:service_slug>/', ServiceOffersListView.as_view(), name='service_offers_list'),
]