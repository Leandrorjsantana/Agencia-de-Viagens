# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response

# Importa os modelos de dados necessários
from site_settings.models import SiteConfiguration
from menus.models import TopBarLink, MenuItem, SocialMediaLink
from services.models import Service
from banners.models import Banner
from promotions.models import PromotionCard # <-- GARANTA QUE ESTA LINHA EXISTA

# Importa o serializer principal
from .serializers import SiteDataSerializer

# Importa o serviço de câmbio
from exchange.services import get_currency_rates

class SiteDataAPIView(APIView):
    """
    Esta API centraliza todos os dados necessários para renderizar
    as partes principais do site (header, footer, homepage, etc.).
    """
    def get(self, request, *args, **kwargs):
        # Busca os dados de cada aplicação
        site_config = SiteConfiguration.objects.first()
        top_bar_links = TopBarLink.objects.all()
        main_menu_items = MenuItem.objects.all()
        social_media_links = SocialMediaLink.objects.all()
        services = Service.objects.filter(is_active=True)
        banners = Banner.objects.filter(is_active=True)
        currency_rates = get_currency_rates()

        # ===================================================================
        # LINHA FALTANDO: Busca os cards de promoção ativos no banco de dados.
        # ===================================================================
        promotion_cards = PromotionCard.objects.filter(is_active=True)

        # Monta um dicionário com todos os dados
        data = {
            'site_configuration': site_config,
            'top_bar_links': top_bar_links,
            'main_menu_items': main_menu_items,
            'social_media_links': social_media_links,
            'services': services,
            'banners': banners,
            'currency_rates': currency_rates,
            # ===================================================================
            # LINHA FALTANDO: Adiciona os cards ao "pacote" de dados.
            # ===================================================================
            'promotion_cards': promotion_cards,
        }

        # Passa os dados para o serializer, que vai converter para JSON
        serializer = SiteDataSerializer(data, context={'request': request})
        
        return Response(serializer.data)