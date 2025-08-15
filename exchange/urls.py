# exchange/urls.py
from django.urls import path
from .views import ExchangeRatesView

urlpatterns = [
    # O endereço será: /api/v1/exchange/rates/
    path('rates/', ExchangeRatesView.as_view(), name='exchange_rates'),
]