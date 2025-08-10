from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from site_settings.models import SiteConfiguration
from menus.models import TopBarLink, MenuItem, SocialMediaLink
from services.models import Service

# Importando o Serializer principal do nosso app 'core'
from .serializers import SiteDataSerializer

class SiteDataAPIView(APIView):
    """
    Esta API entrega todos os dados essenciais para a construção do
    layout principal do site.
    """
    def get(self, request, *args, **kwargs):
        # Busca a primeira (e única) configuração do site.
        site_config = SiteConfiguration.objects.first()
        
        # Se não houver configuração, cria uma para evitar erros.
        if not site_config:
            site_config = SiteConfiguration.objects.create()

        # Busca os outros dados, ordenados.
        top_bar_links = TopBarLink.objects.all()
        main_menu_items = MenuItem.objects.all()
        social_media_links = SocialMediaLink.objects.all()
        
        # CORREÇÃO: Apenas buscamos os serviços ativos. O serializer fará o resto.
        services = Service.objects.filter(is_active=True)

        # Monta um dicionário com todos os dados para o serializer.
        data = {
            'site_configuration': site_config,
            'top_bar_links': top_bar_links,
            'main_menu_items': main_menu_items,
            'social_media_links': social_media_links,
            'services': services,
        }
        
        # Usa o SiteDataSerializer para formatar os dados para a API.
        serializer = SiteDataSerializer(data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
