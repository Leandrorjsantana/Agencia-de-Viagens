# offers/serializers.py

from rest_framework import serializers
from .models import Offer

class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para fornecer todos os detalhes de uma única oferta.
    """
    class Meta:
        model = Offer
        # '__all__' garante que todos os campos do modelo sejam incluídos.
        fields = '__all__'