# site_settings/models.py

from django.db import models
from colorfield.fields import ColorField

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default='Agência de Viagens')
    logo = models.ImageField(
        upload_to='logos/',
        blank=True,
        null=True,
        help_text="Dimensão recomendada: 250x80 pixels"
    )
    # NOVO: Campo para controlar o tamanho do logo
    logo_height = models.PositiveIntegerField(
        default=50,
        help_text="Altura do logo em pixels (ex: 50). A largura será ajustada automaticamente."
    )
    # ATUALIZADO: Campo de cor com seletor visual
    primary_color = ColorField(
        default='#0d6efd',
        help_text="Cor principal do site"
    )
    footer_text = models.TextField(blank=True, help_text="Texto que aparecerá no rodapé do site.")

    def __str__(self):
        return "Configurações Gerais do Site"

    class Meta:
        verbose_name = "Configuração Geral do Site"
        verbose_name_plural = "Configurações Gerais do Site"