# leads/models.py

from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Lead(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Novo'),
        ('CONTACTED', 'Contactado'),
        ('CONVERTED', 'Convertido em Venda'),
        ('LOST', 'Perdido'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Oferta de Interesse")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Status da Solicitação")
    
    full_name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail")
    phone_number = models.CharField(max_length=20, verbose_name="Telefone / WhatsApp")
    
    travel_date = models.DateField(null=True, blank=True, verbose_name="Data de Viagem Pretendida")
    number_of_people = models.PositiveIntegerField(default=1, verbose_name="Número de Pessoas")
    observations = models.TextField(blank=True, verbose_name="Observações do Cliente")

    client_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário Cliente (se logado)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.full_name} para {self.offer.title if self.offer else 'Consulta Geral'}"

    class Meta:
        ordering = ['-created_at']
        # CORREÇÃO AQUI: Mudando os nomes que aparecem no admin
        verbose_name = "Solicitação de Reserva"
        verbose_name_plural = "Solicitações de Reserva"