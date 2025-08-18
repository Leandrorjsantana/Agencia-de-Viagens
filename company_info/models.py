# company_info/models.py
from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Membro")
    role = models.CharField(max_length=100, verbose_name="Cargo")
    photo = models.ImageField(upload_to='team/', help_text="Dimensão recomendada: 400x400 pixels (quadrada)")
    bio = models.CharField(max_length=255, blank=True, verbose_name="Mini Frase de Apresentação")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Membro da Equipa"
        verbose_name_plural = "Equipe"