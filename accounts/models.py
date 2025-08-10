# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

# Este modelo guarda as informações adicionais de cada usuário.
class Profile(models.Model):
    # Este campo cria um link direto e único com o sistema de usuários do Django.
    # Se um usuário for deletado, seu perfil também será.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Campos para o cadastro completo do cliente
    full_name = models.CharField(max_length=255, blank=True, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefone / WhatsApp")
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    logradouro = models.CharField(max_length=255, blank=True, verbose_name="Logradouro")
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, verbose_name="Estado (UF)")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfis de Clientes"