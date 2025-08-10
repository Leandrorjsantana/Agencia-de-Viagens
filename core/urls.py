# core/urls.py

from django.urls import path
from .views import SiteDataAPIView

urlpatterns = [
    # O endereço será: /api/v1/site-data/
    path('site-data/', SiteDataAPIView.as_view(), name='site_data'),
]