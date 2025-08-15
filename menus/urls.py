# menus/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet

router = DefaultRouter()
router.register(r'', MenuViewSet, basename='menu')

app_name = 'menus'

urlpatterns = [
    path('', include(router.urls)),
]