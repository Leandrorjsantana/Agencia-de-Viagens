# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    # Define qual "molde" usar para criar o objeto
    serializer_class = RegisterSerializer
    # Define que qualquer pessoa (mesmo não logada) pode acessar esta API
    permission_classes = [permissions.AllowAny]
    # Define o conjunto de dados base (não é estritamente necessário para 'create', mas é uma boa prática)
    queryset = User.objects.all()