# core/serializers.py

from rest_framework import serializers
from site_settings.models import SiteConfiguration
from menus.models import TopBarLink, MenuItem, SocialMediaLink
from services.models import Service
from offers.models import Offer
from banners.models import Banner # Importa o modelo de Banner

# Molde para os Banners
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'subtitle', 'image', 'link_url')

# (O resto dos seus serializers... SiteConfigurationSerializer, OfferSerializer, etc.)
# ...
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
    offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'icon_class', 
            'form_fields', 'section_headline', 'offers'
        )

    def get_offers(self, service_instance):
        offers_queryset = Offer.objects.filter(
            service=service_instance, 
            is_active=True, 
            show_on_landing_page=True
        )
        return OfferSerializer(offers_queryset, many=True).data

# Molde principal que junta tudo
class SiteDataSerializer(serializers.Serializer):
    site_configuration = SiteConfigurationSerializer()
    top_bar_links = TopBarLinkSerializer(many=True)
    main_menu_items = MenuItemSerializer(many=True)
    social_media_links = SocialMediaLinkSerializer(many=True)
    services = ServiceSerializer(many=True)
    banners = BannerSerializer(many=True) # Adiciona os banners ao pacote