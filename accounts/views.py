# accounts/views.py

from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

# --------------------------------------------------------------------
# NOVO: View para o perfil do usuário logado
# --------------------------------------------------------------------
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para um usuário ver e atualizar seu próprio perfil.
    Acessível apenas por usuários autenticados.
    """
    serializer_class = UserProfileSerializer
    # Esta é a "chave" da segurança: só permite o acesso se o usuário estiver logado.
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Este método garante que a view sempre retorne os dados
        # do usuário que está fazendo a requisição, e não de outro.
        return self.request.user