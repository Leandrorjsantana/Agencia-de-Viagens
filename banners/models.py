# banners/models.py

from django.db import models
# A linha 'from adminsortable2.models import SortableMixin' foi REMOVIDA.

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título (para controlo interno)")
    subtitle = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo (opcional)")
    image = models.ImageField(upload_to='banners/', verbose_name="Imagem do Banner", help_text="Dimensão recomendada: 1920x450 pixels.")
    link_url = models.URLField(max_length=255, blank=True, verbose_name="URL de Destino (opcional)")
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Banner da Página Inicial"
        verbose_name_plural = "Banners da Página Inicial"