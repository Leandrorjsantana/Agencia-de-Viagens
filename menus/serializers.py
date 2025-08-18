# menus/serializers.py

from rest_framework import serializers
from .models import TopBarLink, MenuItem, SocialMediaLink

class TopBarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBarLink
        # --- CORREÇÃO APLICADA AQUI ---
        fields = ('id', 'title', 'url', 'icon_class', 'open_in_new_tab')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'url', 'is_external')

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('id', 'name', 'url', 'icon_class')