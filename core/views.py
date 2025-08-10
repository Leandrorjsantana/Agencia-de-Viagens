# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from site_settings.models import SiteConfiguration
from menus.models import TopBarLink, MenuItem, SocialMediaLink
from services.models import Service
from banners.models import Banner # Importa o modelo de Banner

from .serializers import SiteDataSerializer

class SiteDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        site_config = SiteConfiguration.objects.first()
        if not site_config:
            site_config = SiteConfiguration.objects.create()

        top_bar_links = TopBarLink.objects.all()
        main_menu_items = MenuItem.objects.all()
        social_media_links = SocialMediaLink.objects.all()
        services = Service.objects.filter(is_active=True)
        banners = Banner.objects.filter(is_active=True) # Busca os banners ativos

        data = {
            'site_configuration': site_config,
            'top_bar_links': top_bar_links,
            'main_menu_items': main_menu_items,
            'social_media_links': social_media_links,
            'services': services,
            'banners': banners, # Adiciona os banners ao pacote de dados
        }
        
        serializer = SiteDataSerializer(data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)