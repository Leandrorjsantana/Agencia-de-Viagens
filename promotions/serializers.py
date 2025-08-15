# promotions/serializers.py
from rest_framework import serializers
from .models import PromotionCard

class PromotionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCard
        fields = ('image', 'link_url')