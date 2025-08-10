# site_settings/models.py

from django.db import models
from colorfield.fields import ColorField

class SiteConfiguration(models.Model):
    # Seção de Identidade Visual
    site_name = models.CharField(max_length=255, default='Agência de Viagens', verbose_name="Nome do Site")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Dimensão recomendada: 250x80 pixels")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text="Ícone quadrado. Dimensão recomendada: 64x64 pixels.", verbose_name="Favicon do Site")
    logo_height = models.PositiveIntegerField(default=50, help_text="Altura do logo em pixels (ex: 50).", verbose_name="Altura do Logo (em pixels)")

    # Seção do Formulário de Busca (Hero)
    hero_background_color = ColorField(default='#333333', verbose_name="Cor de Fundo da Busca")
    hero_background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text="Opcional. Dimensão recomendada: 1920x500 pixels.", verbose_name="Imagem de Fundo da Busca")
    
    # Seção da Newsletter
    newsletter_headline = models.CharField(max_length=100, blank=True, verbose_name="Título da Newsletter")
    newsletter_subheadline = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo da Newsletter")
    newsletter_button_text = models.CharField(max_length=50, default='Inscrever-se', verbose_name="Texto do Botão da Newsletter")
    newsletter_background_color = ColorField(default='#212529', verbose_name="Cor de Fundo da Newsletter")
    newsletter_background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text="Opcional. Dimensão recomendada: 1920x400 pixels.", verbose_name="Imagem de Fundo da Newsletter")

    # NOVO: Seção de Carrosséis
    banner_autoplay_speed = models.PositiveIntegerField(
        default=5000,
        help_text="Velocidade em milissegundos (ex: 5000 para 5 segundos). Digite 0 para desativar.",
        verbose_name="Velocidade do Carrossel de Banners (ms)"
    )
    offer_carousel_speed = models.PositiveIntegerField(
        default=0,
        help_text="Velocidade em milissegundos (ex: 4000 para 4 segundos). Digite 0 para desativar.",
        verbose_name="Velocidade do Carrossel de Ofertas (ms)"
    )

    # Fontes e Cores Globais
    main_font = models.CharField(max_length=100, default='Poppins', verbose_name="Fonte Principal")
    primary_color = ColorField(default='#0d6efd', verbose_name="Cor Primária (Botões e Links)")
    top_bar_bg_color = ColorField(default='#F8F9FA', verbose_name="Fundo da Barra Superior")
    top_bar_text_color = ColorField(default='#6C757D', verbose_name="Texto da Barra Superior")
    main_header_bg_color = ColorField(default='#FFFFFF', verbose_name="Fundo do Cabeçalho Principal")
    main_header_text_color = ColorField(default='#333333', verbose_name="Texto do Cabeçalho Principal")
    footer_bg_color = ColorField(default='#212529', verbose_name="Fundo do Rodapé")
    footer_text_color = ColorField(default='#FFFFFF', verbose_name="Texto do Rodapé")
    
    footer_text = models.TextField(blank=True, verbose_name="Texto do Rodapé")
    seo_title = models.CharField(max_length=60, blank=True, verbose_name="Título para o Google")
    seo_description = models.TextField(max_length=160, blank=True, verbose_name="Descrição para o Google")
    tracking_header_scripts = models.TextField(blank=True, verbose_name="Scripts no Cabeçalho (<head>)")
    tracking_body_start_scripts = models.TextField(blank=True, verbose_name="Scripts no Início do Corpo (<body>)")
    tracking_body_end_scripts = models.TextField(blank=True, verbose_name="Scripts no Fim do Corpo (</body>)")

    def __str__(self):
        return "Configurações Gerais do Site"

    class Meta:
        verbose_name = "Configuração Geral do Site"