# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from site_settings.models import SiteConfiguration
from site_settings.serializers import SiteConfigurationSerializer
from menus.models import TopBarLink, MenuItem
from menus.serializers import TopBarLinkSerializer, MenuItemSerializer

class SiteDataAPIView(APIView):
    """
    Esta API entrega todos os dados essenciais para a construção do
    layout principal do site (cabeçalho, rodapé, etc.).
    """
    def get(self, request, *args, **kwargs):
        # Tenta buscar a primeira (e única) configuração do site.
        # Se não existir, cria uma com valores padrão.
        site_config, created = SiteConfiguration.objects.get_or_create(pk=1)
        
        # Busca todos os links dos menus, ordenados.
        top_bar_links = TopBarLink.objects.all().order_by('order')
        main_menu_items = MenuItem.objects.all().order_by('order')

        # Serializa os dados para o formato JSON.
        config_serializer = SiteConfigurationSerializer(site_config)
        top_bar_serializer = TopBarLinkSerializer(top_bar_links, many=True)
        main_menu_serializer = MenuItemSerializer(main_menu_items, many=True)

        # Monta o pacote de dados final.
        data = {
            'site_configuration': config_serializer.data,
            'top_bar_links': top_bar_serializer.data,
            'main_menu_items': main_menu_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)