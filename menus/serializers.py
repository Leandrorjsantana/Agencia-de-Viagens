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

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        # CORRIGIDO: O campo 'platform' foi trocado por 'name', que é o campo correto no seu models.py
        fields = ('id', 'name', 'url', 'icon_class')