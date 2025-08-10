# accounts/urls.py

from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    # Rota para o cadastro (já existia)
    path('register/', RegisterView.as_view(), name='register'),
    
    # --- NOVA ROTA ADICIONADA ---
    # O endereço será: /api/v1/accounts/profile/
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]