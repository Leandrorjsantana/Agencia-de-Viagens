# services/serializers.py

from rest_framework import serializers
from .models import Service
from offers.models import Offer

class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para as ofertas dentro de um serviço.
    """
    class Meta:
        model = Offer
        # Incluímos todos os campos necessários para o card de oferta
        fields = (
            'id', 'title', 'subtitle', 'slug', 'image', 'details',
            'hotel_name', 'hotel_rating', 'price', 'original_price',
            'price_per_person', 'taxes_included', 'origin', 
            'duration_days', 'duration_nights', 'promo_tag', 'highlight_button'
        )

class ServiceWithOffersSerializer(serializers.ModelSerializer):
    """
    Serializer para um serviço, incluindo uma lista das suas ofertas em destaque.
    """
    # Aninha as ofertas que estão marcadas para aparecer na página inicial
    offers = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'icon_class', 'form_fields', 
            'section_headline', 'offers'
        )
    
    def get_offers(self, obj):
        # Filtra apenas as ofertas que devem ser mostradas na landing page
        offers_queryset = obj.offers.filter(show_on_landing_page=True, is_active=True)
        return OfferSerializer(offers_queryset, many=True, context=self.context).data
