# pages/urls.py

from django.urls import path
from .views import PageDetailView  # <-- Esta linha agora vai funcionar

urlpatterns = [
    path('<slug:slug>/', PageDetailView.as_view(), name='page-detail'),
]