# accounts/urls.py

from django.urls import path
from .views import RegisterView

urlpatterns = [
    # O endereço será: /api/v1/accounts/register/
    path('register/', RegisterView.as_view(), name='register'),
]