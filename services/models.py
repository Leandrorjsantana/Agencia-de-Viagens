# services/models.py

from django.db import models
# A linha 'from adminsortable2.models import SortableMixin' foi REMOVIDA.

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Serviço")
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=100, blank=True, verbose_name="Classe do Ícone")
    form_fields = models.JSONField(
        blank=True, null=True, 
        verbose_name="Campos do Formulário de Busca (JSON)",
        help_text="Defina os campos para o formulário de busca deste serviço."
    )
    section_headline = models.CharField(
        max_length=255, blank=True, 
        verbose_name="Título da Seção de Ofertas na Home",
        help_text="Ex: 'Ofertas Incríveis de Hospedagem'"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"