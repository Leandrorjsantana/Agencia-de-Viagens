# menus/serializers.py

from rest_framework import serializers
from .models import TopBarLink, MenuItem

class TopBarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBarLink
        fields = ('id', 'title', 'url', 'icon_class')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'url', 'is_external')