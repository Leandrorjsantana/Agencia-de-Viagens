# reservations/models.py

from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Aguardando Pagamento'),
        ('CONFIRMED', 'Confirmada'),
        ('CANCELED', 'Cancelada'),
        ('COMPLETED', 'Concluída'),
    ]

    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reservations', verbose_name="Cliente")
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations', verbose_name="Oferta Associada (Opcional)")
    
    reservation_code = models.CharField(max_length=20, unique=True, verbose_name="Código da Reserva")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    start_date = models.DateField(verbose_name="Data de Início da Viagem")
    end_date = models.DateField(verbose_name="Data de Fim da Viagem")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Total (R$)")
    notes = models.TextField(blank=True, verbose_name="Observações Internas (só para o admin)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva {self.reservation_code} - {self.client.username}"

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

class ReservationDocument(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='documents', verbose_name="Reserva")
    description = models.CharField(max_length=100, verbose_name="Descrição do Documento (ex: Voucher, Bilhete Aéreo)")
    file = models.FileField(upload_to='reservation_documents/', verbose_name="Arquivo")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento para a Reserva {self.reservation.reservation_code}"

    class Meta:
        verbose_name = "Documento da Reserva"
        verbose_name_plural = "Documentos da Reserva"