# help_center/models.py

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# A linha 'from adminsortable2.models import SortableMixin' foi REMOVIDA.

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class HelpCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título da Categoria")
    slug = models.SlugField(unique=True, help_text="Versão do título para a URL (ex: faturamento-e-reembolso)")
    icon_class = models.CharField(max_length=50, blank=True, verbose_name="Classe do Ícone (Font Awesome)", help_text="Ex: fa-solid fa-file-invoice-dollar")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Categoria de Ajuda"
        verbose_name_plural = "Categorias de Ajuda"

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class HelpArticle(models.Model):
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, related_name="articles", verbose_name="Categoria")
    question = models.CharField(max_length=255, verbose_name="Pergunta")
    answer = RichTextUploadingField(verbose_name="Resposta")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name = "Artigo de Ajuda"
        verbose_name_plural = "Artigos de Ajuda"