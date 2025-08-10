# offers/models.py

from django.db import models
from services.models import Service

class Offer(models.Model):
    # Relacionamentos
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='offers', 
        verbose_name="Serviço"
    )

    # Informações Principais
    title = models.CharField(max_length=255, verbose_name="Título Principal")
    subtitle = models.CharField(max_length=255, verbose_name="Subtítulo")
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to='offers/', blank=True, null=True, 
        verbose_name="Imagem do Card",
        help_text="Dimensão recomendada: 400x300 pixels"
    )
    details = models.TextField(blank=True, verbose_name="Detalhes (um por linha)")

    # Preços
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Preço Final")
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        verbose_name="Preço Original (para mostrar desconto)"
    )
    price_per_person = models.BooleanField(default=True, verbose_name="É preço por pessoa?")
    taxes_included = models.BooleanField(default=True, verbose_name="Taxas inclusas?")

    # Detalhes da Viagem
    origin = models.CharField(max_length=100, blank=True, verbose_name="Origem (ex: Saindo de São Paulo)")
    duration_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duração (Dias)")
    duration_nights = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duração (Noites)")

    # Controles de Exibição
    promo_tag = models.CharField(max_length=50, blank=True, verbose_name="Tag Promocional (ex: 30% OFF)")
    highlight_button = models.BooleanField(default=False, verbose_name="Destacar Botão 'Reservar'?")
    is_active = models.BooleanField(default=True, verbose_name="Ativa?")
    show_on_landing_page = models.BooleanField(default=False, verbose_name="Mostrar na Página Inicial?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"