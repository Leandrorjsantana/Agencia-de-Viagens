# accounts/urls.py

from django.urls import path
# Adicionada a nova view na importação
from .views import RegisterView, UserProfileView, UserFullNameView

app_name = 'accounts'

urlpatterns = [
    # Rota para o cadastro (já existia)
    path('register/', RegisterView.as_view(), name='register'),
    
    # Rota para o perfil do cliente
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # --- ROTA NOVA ADICIONADA ---
    # Rota para o admin buscar o nome completo de um usuário
    # Ex: /api/v1/accounts/get-full-name/5/
    path('get-full-name/<int:pk>/', UserFullNameView.as_view(), name='user_full_name'),
]