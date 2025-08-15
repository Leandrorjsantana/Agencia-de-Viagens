# core/serializers.py

from rest_framework import serializers

# Importa os serializers de cada aplicação
from site_settings.serializers import SiteConfigurationSerializer
from menus.serializers import TopBarLinkSerializer, MenuItemSerializer, SocialMediaLinkSerializer
from services.serializers import ServiceWithOffersSerializer
from banners.serializers import BannerSerializer
from promotions.serializers import PromotionCardSerializer # <-- 1. IMPORTE O SERIALIZER DE PROMOÇÕES

class CurrencyRateSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    bid = serializers.CharField()

class SiteDataSerializer(serializers.Serializer):
    """
    Define a estrutura do grande objeto JSON que a API vai retornar.
    Cada campo aqui corresponde a uma chave no JSON final.
    """
    site_configuration = SiteConfigurationSerializer()
    top_bar_links = TopBarLinkSerializer(many=True)
    main_menu_items = MenuItemSerializer(many=True)
    social_media_links = SocialMediaLinkSerializer(many=True)
    services = ServiceWithOffersSerializer(many=True)
    banners = BannerSerializer(many=True)
    currency_rates = CurrencyRateSerializer(many=True, required=False)

    # ===================================================================
    #   2. ADICIONE O CAMPO FALTANDO AQUI
    # ===================================================================
    promotion_cards = PromotionCardSerializer(many=True, required=False)