# exchange/views.py
import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import CurrencyRateSerializer

class ExchangeRatesView(APIView):
    """
    Busca as cotações de moedas da AwesomeAPI e as guarda em cache.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        currency_pairs = 'USD-BRL,USDT-BRL,EUR-BRL,GBP-BRL,ARS-BRL,CAD-BRL,CHF-BRL,BTC-BRL,JPY-BRL'
        
        # --- CORREÇÃO DEFINITIVA: Mudando a chave do cache mais uma vez para garantir ---
        cache_key = 'exchange_rates_cache_v3'
        cached_rates = cache.get(cache_key)

        if cached_rates:
            return Response(cached_rates)

        api_url = f"https://economia.awesomeapi.com.br/json/last/{currency_pairs}"
        
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            formatted_data = []
            for key, value in data.items():
                # Renomeia o Dólar Turismo para o diferenciar
                if value.get('code') == 'USDT':
                    value['name'] = 'Dólar Turismo/Real Brasileiro'
                formatted_data.append(value)

            serializer = CurrencyRateSerializer(formatted_data, many=True)
            
            cache.set(cache_key, serializer.data, 60 * 30)
            
            return Response(serializer.data)

        except requests.RequestException as e:
            print(f"Erro ao buscar cotações de câmbio: {e}")
            return Response({"error": "Não foi possível buscar as cotações."}, status=500)