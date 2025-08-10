from rest_framework import serializers
from site_settings.models import SiteConfiguration
from menus.models import TopBarLink, MenuItem, SocialMediaLink
from services.models import Service
from offers.models import Offer

# Cada classe abaixo é um "molde" para um tipo de dado específico.

class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'

class TopBarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBarLink
        fields = ('id', 'title', 'url', 'icon_class')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'url', 'is_external')

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('id', 'name', 'url', 'icon_class')

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id', 'title', 'subtitle', 'slug', 'image', 'price', 
            'promo_tag', 'origin', 'duration_days', 'duration_nights', 
            'details', 'original_price', 'price_per_person', 
            'taxes_included', 'highlight_button'
        )

class ServiceSerializer(serializers.ModelSerializer):
    # CORREÇÃO: Usando um SerializerMethodField para filtrar as ofertas corretamente.
    offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'icon_class', 
            'form_fields', 'section_headline', 'offers'
        )

    def get_offers(self, service_instance):
        # Este método filtra as ofertas para cada serviço individualmente.
        offers_queryset = Offer.objects.filter(
            service=service_instance, 
            is_active=True, 
            show_on_landing_page=True
        )
        # Serializa apenas as ofertas filtradas.
        return OfferSerializer(offers_queryset, many=True).data

# Este é o "molde" principal que junta todos os outros em um único pacote.
class SiteDataSerializer(serializers.Serializer):
    site_configuration = SiteConfigurationSerializer()
    top_bar_links = TopBarLinkSerializer(many=True)
    main_menu_items = MenuItemSerializer(many=True)
    social_media_links = SocialMediaLinkSerializer(many=True)
    services = ServiceSerializer(many=True)
    # Banners e outras seções serão adicionados aqui no futuro.
