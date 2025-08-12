# pages/serializers.py

from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    """
    Serializer para fornecer todos os detalhes de uma única página de conteúdo.
    """
    class Meta:
        model = Page
        # Define os campos que a API irá entregar
        fields = ('title', 'slug', 'content', 'seo_title', 'seo_description')