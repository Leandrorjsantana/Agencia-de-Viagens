# banners/serializers.py
from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Banner.
    Converte os dados do banner para o formato JSON.
    """
    class Meta:
        model = Banner
        # Define os campos que serão expostos na API.
        fields = [
            'id', 
            'title', 
            'subtitle', 
            'image', 
            'link', 
            'is_active',
            'order'
        ]