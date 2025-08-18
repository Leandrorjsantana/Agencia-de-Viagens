# menus/serializers.py

from rest_framework import serializers
from .models import TopBarLink, MenuItem, SocialMediaLink

class TopBarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBarLink
        fields = ('id', 'title', 'url', 'icon_class')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'url')

# --- CORREÇÃO AQUI: Usando os campos corretos do modelo ---
class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        # O campo 'platform' foi trocado de volta para 'title', que é o campo correto.
        fields = ('id', 'title', 'url', 'icon_class')