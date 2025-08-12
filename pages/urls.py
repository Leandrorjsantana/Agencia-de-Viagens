# pages/urls.py

from django.urls import path
from .views import PageDetailView

urlpatterns = [
    # O endereço será: /api/v1/pages/<slug-da-pagina>/
    # ex: /api/v1/pages/quem-somos/
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]