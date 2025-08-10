# banners/models.py

from django.db import models
# A linha 'from adminsortable2.models import SortableMixin' foi REMOVIDA.

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name="Título do Banner")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo do Banner")
    image = models.ImageField(
        upload_to='banners/',
        help_text="Dimensão recomendada: 1920x600 pixels"
    )
    link_url = models.URLField(max_length=255, blank=True, verbose_name="URL do Link")
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f"Banner {self.id}"

    class Meta:
        ordering = ['order']
        verbose_name = "Banner"
        verbose_name_plural = "Banners da Página Inicial"