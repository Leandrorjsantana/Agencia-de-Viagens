# insurance/models.py

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# A classe agora é um modelo padrão do Django, sem heranças especiais.
class InsuranceBenefit(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título do Benefício")
    description = models.TextField(verbose_name="Descrição Curta")
    
    # --- NOVO CAMPO ADICIONADO AQUI ---
    long_description = RichTextUploadingField(
        blank=True, 
        verbose_name="Descrição Longa (Opcional)",
        help_text="Use este campo para um texto mais detalhado com formatação, imagens e links."
    )

    icon_class = models.CharField(max_length=50, blank=True, verbose_name="Classe do Ícone (Font Awesome)", help_text="Ex: fa-solid fa-user-doctor")
    
    # Este é o campo que a biblioteca usará para ordenar.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Benefício do Seguro Viagem"
        verbose_name_plural = "Benefícios do Seguro Viagem"

class InsurancePlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Plano")
    price_info = models.CharField(max_length=50, blank=True, verbose_name="Informação de Preço", help_text="Ex: A partir de R$ 29,90/dia")
    features = RichTextUploadingField(verbose_name="Características (uma por linha)")
    is_popular = models.BooleanField(default=False, verbose_name="É o plano mais popular?")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Plano de Seguro Viagem"
        verbose_name_plural = "Planos de Seguro Viagem"

class InsuranceFAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Pergunta")
    answer = models.TextField(verbose_name="Resposta")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name = "Pergunta Frequente (Seguro)"
        verbose_name_plural = "Perguntas Frequentes (Seguro)"

class TrustSeal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Selo/Parceiro")
    logo = models.ImageField(upload_to='seals/', verbose_name="Logo")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Selo de Confiança / Parceiro"
        verbose_name_plural = "Selos de Confiança / Parceiros"