# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(unique=True, help_text="Versão do nome para a URL, sem espaços ou acentos.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Tag")
    slug = models.SlugField(unique=True, help_text="Versão do nome para a URL, sem espaços ou acentos.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título do Post")
    slug = models.SlugField(unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Autor")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    
    featured_image = models.ImageField(
        upload_to='blog_featured/', 
        verbose_name="Imagem Destacada",
        help_text="Dimensão recomendada: 1200x600 pixels."
    )
    summary = models.TextField(max_length=200, verbose_name="Resumo (até 200 caracteres)")
    content = RichTextUploadingField(verbose_name="Conteúdo do Post")

    is_published = models.BooleanField(default=False, verbose_name="Publicado?")
    is_pinned = models.BooleanField(default=False, verbose_name="Fixar no Topo?")
    
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_pinned', '-published_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class BlogAdBanner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Anúncio (para controlo interno)")
    image = models.ImageField(upload_to='blog_ads/', verbose_name="Imagem do Banner")
    link_url = models.URLField(max_length=255, verbose_name="URL de Destino")
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Banner de Publicidade (Blog)"
        verbose_name_plural = "Banners de Publicidade (Blog)"

# --- NOVO MODELO PARA OS COMENTÁRIOS ---
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Conteúdo")
    
    # Para suportar respostas a comentários
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="Comentário Pai")
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="Aprovado?")

    def __str__(self):
        return f"Comentário de {self.author.username} em {self.post.title}"

    class Meta:
        ordering = ['created_at']
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"