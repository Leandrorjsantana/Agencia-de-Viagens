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
        fields = ('id', 'title', 'url', 'is_external')

# --- CORREÇÃO AQUI: Usando o campo 'name' que está no seu models.py ---
class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('id', 'name', 'url', 'icon_class')
