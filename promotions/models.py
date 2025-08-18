# promotions/models.py
from django.db import models

class PromotionCard(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título (para controlo interno)")
    image = models.ImageField(upload_to='promotions/', verbose_name="Imagem do Card", help_text="Dimensão recomendada: 400x400 pixels (quadrada).")
    link_url = models.URLField(max_length=255, verbose_name="URL de Destino")
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Card de Promoção"
        verbose_name_plural = "Cards de Promoção"