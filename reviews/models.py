# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Oferta Avaliada (Opcional)"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Autor da Avaliação"
    )

    title = models.CharField(max_length=200, verbose_name="Título da Avaliação")
    content = models.TextField(verbose_name="Conteúdo da Avaliação")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name="Nota (de 1 a 5)"
    )
    
    # ADICIONANDO O CAMPO DE FOTO DE VOLTA
    photo = models.ImageField(
        upload_to='review_photos/',
        blank=True,
        null=True,
        verbose_name="Foto da Viagem"
    )

    is_approved = models.BooleanField(default=False, verbose_name="Aprovada?")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        if self.offer:
            return f"Avaliação de {self.author.username} para '{self.offer.title}'"
        return f"Avaliação geral de {self.author.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avaliação de Cliente"
        verbose_name_plural = "Avaliações de Clientes"