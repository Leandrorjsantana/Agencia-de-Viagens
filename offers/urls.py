# offers/urls.py
from django.urls import path
from .views import OfferDetailView, ServiceOffersListView, OfferForAdminView

urlpatterns = [
    # Rota para a página de detalhes de uma oferta (pública)
    path('<slug:slug>/', OfferDetailView.as_view(), name='offer_detail'),

    # Rota para a lista de ofertas de um serviço (pública)
    path('servico/<slug:service_slug>/', ServiceOffersListView.as_view(), name='service_offers_list'),
    
    # Rota para o painel de administração buscar os detalhes de uma oferta (privada)
    path('admin-details/<int:pk>/', OfferForAdminView.as_view(), name='offer_admin_details'),
]
