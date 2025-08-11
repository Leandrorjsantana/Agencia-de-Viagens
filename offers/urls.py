# offers/urls.py

from django.urls import path
from .views import OfferDetailView

urlpatterns = [
    # O endereço será: /api/v1/offers/<slug-da-oferta>/
    # ex: /api/v1/offers/pacote-para-o-ceara/
    path('<slug:slug>/', OfferDetailView.as_view(), name='offer_detail'),
]