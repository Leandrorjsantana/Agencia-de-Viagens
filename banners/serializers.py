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
        # CORRIGIDO: O campo 'link' foi trocado por 'link_url'.
        fields = (
            'id', 
            'title', 
            'subtitle', 
            'image', 
            'link_url', 
            'is_active',
            'order'
        )