# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # NOVO CAMPO: Foto de Perfil
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True,
        verbose_name="Foto de Perfil"
    )

    full_name = models.CharField(max_length=255, blank=True, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefone / WhatsApp")
    
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