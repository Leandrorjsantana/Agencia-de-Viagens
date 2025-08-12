# pages/models.py

from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título da Página")
    slug = models.SlugField(unique=True, help_text="Usado na URL da página (ex: quem-somos)")
    content = models.TextField(verbose_name="Conteúdo da Página", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Página de Conteúdo"
        verbose_name_plural = "Páginas de Conteúdo"
        ordering = ['title']