# banners/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet

# Cria um roteador para a API
router = DefaultRouter()

# Registra a nossa ViewSet de Banners com o roteador.
# Isso vai criar automaticamente as rotas para listagem, detalhe, criação, etc.
# O 'basename' é importante para a geração dos nomes das URLs.
router.register(r'', BannerViewSet, basename='banner')

app_name = 'banners'

urlpatterns = [
    # Inclui todas as URLs geradas pelo roteador.
    path('', include(router.urls)),
]