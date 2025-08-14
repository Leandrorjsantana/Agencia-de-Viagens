# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Estrela'), (2, '2 Estrelas'), (3, '3 Estrelas'),
        (4, '4 Estrelas'), (5, '5 Estrelas'),
    ]

    # CORREÇÃO: A oferta agora é opcional
    offer = models.ForeignKey(
        Offer, on_delete=models.SET_NULL, null=True, blank=True, 
        verbose_name="Oferta Avaliada (Opcional)"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor (Cliente)")
    
    title = models.CharField(max_length=200, verbose_name="Título da Avaliação")
    content = models.TextField(verbose_name="Conteúdo da Avaliação")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Nota (Estrelas)")
    
    # NOVO CAMPO: Foto enviada pelo cliente
    photo = models.ImageField(
        upload_to='review_photos/', blank=True, null=True,
        verbose_name="Foto da Viagem (Opcional)",
        help_text="Uma foto enviada pelo cliente para ilustrar a experiência."
    )
    
    is_approved = models.BooleanField(default=True, verbose_name="Aprovada?")
    is_featured = models.BooleanField(default=False, verbose_name="Destacar na Página Inicial?")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.author.username} para {self.offer.title if self.offer else 'avaliação geral'}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avaliação de Cliente"
        verbose_name_plural = "Avaliações de Clientes"