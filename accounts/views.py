# accounts/views.py

from rest_framework import generics, permissions
# Adicionado Response para a nova view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

# --------------------------------------------------------------------
# View para o perfil do usuário logado
# --------------------------------------------------------------------
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para um usuário ver e atualizar seu próprio perfil.
    Acessível apenas por usuários autenticados.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Este método garante que a view sempre retorne os dados
        # do usuário que está fazendo a requisição, e não de outro.
        return self.request.user

# --------------------------------------------------------------------
# --- CÓDIGO NOVO ADICIONADO ---
# View segura para o admin buscar o nome completo de um cliente pelo ID.
# --------------------------------------------------------------------
class UserFullNameView(generics.RetrieveAPIView):
    """
    Esta view é usada pelo JavaScript do admin de Reservas para buscar
    o nome completo de um cliente e exibi-lo como confirmação.
    """
    queryset = User.objects.all()
    # Apenas usuários logados no admin podem acessar
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        # Pega a instância do usuário (ex: usuário com ID 5)
        instance = self.get_object()
        # Pega o nome completo (ex: "Leandro Santana")
        full_name = instance.get_full_name()
        
        # Se o usuário não tiver nome completo cadastrado, retorna o username
        display_name = full_name if full_name else instance.username
        
        # Retorna uma resposta JSON simples
        return Response({'full_name': display_name})