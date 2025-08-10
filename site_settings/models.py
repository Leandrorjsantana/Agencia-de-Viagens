# site_settings/models.py

from django.db import models
from colorfield.fields import ColorField

class SiteConfiguration(models.Model):
    # Seção de Identidade Visual
    site_name = models.CharField(max_length=255, default='Agência de Viagens', verbose_name="Nome do Site")
    logo = models.ImageField(
        upload_to='logos/', blank=True, null=True,
        help_text="Dimensão recomendada: 250x80 pixels"
    )
    favicon = models.ImageField(
        upload_to='favicons/', blank=True, null=True,
        help_text="Ícone da aba do navegador. Use uma imagem quadrada (ex: 64x64 pixels).",
        verbose_name="Favicon do Site"
    )
    logo_height = models.PositiveIntegerField(
        default=50,
        help_text="Altura do logo em pixels (ex: 50). A largura será ajustada automaticamente.",
        verbose_name="Altura do Logo (em pixels)"
    )

    # Seção de Fontes e Cores
    main_font = models.CharField(max_length=100, default='Poppins', verbose_name="Fonte Principal")
    primary_color = ColorField(default='#0d6efd', verbose_name="Cor Primária (Botões e Links)")
    top_bar_bg_color = ColorField(default='#F8F9FA', verbose_name="Fundo da Barra Superior")
    top_bar_text_color = ColorField(default='#6C757D', verbose_name="Texto da Barra Superior")
    main_header_bg_color = ColorField(default='#FFFFFF', verbose_name="Fundo do Cabeçalho Principal")
    main_header_text_color = ColorField(default='#333333', verbose_name="Texto do Cabeçalho Principal")
    footer_bg_color = ColorField(default='#212529', verbose_name="Fundo do Rodapé")
    footer_text_color = ColorField(default='#FFFFFF', verbose_name="Texto do Rodapé")
    
    # Seção do Rodapé
    footer_text = models.TextField(blank=True, verbose_name="Texto do Rodapé")

    # Seção de SEO
    seo_title = models.CharField(
        max_length=60, blank=True,
        verbose_name="Título para o Google",
        help_text="O título que aparece na aba do navegador e nos resultados do Google (máx. 60 caracteres)."
    )
    seo_description = models.TextField(
        max_length=160, blank=True,
        verbose_name="Descrição para o Google",
        help_text="O texto que aparece sob o título nos resultados do Google (máx. 160 caracteres)."
    )

    # Seção de Scripts de Rastreamento
    tracking_header_scripts = models.TextField(
        blank=True, verbose_name="Scripts no Cabeçalho (<head>)",
        help_text="Cole aqui os scripts que devem ir antes de </head> (ex: Google Analytics, Pixel do Facebook)."
    )
    tracking_body_start_scripts = models.TextField(
        blank=True, verbose_name="Scripts no Início do Corpo (<body>)",
        help_text="Cole aqui os scripts que devem ir logo após a tag <body> (ex: Google Tag Manager)."
    )
    tracking_body_end_scripts = models.TextField(
        blank=True, verbose_name="Scripts no Fim do Corpo (</body>)",
        help_text="Cole aqui os scripts que devem ir antes de </body>."
    )

    def __str__(self):
        return "Configurações Gerais do Site"

    class Meta:
        verbose_name = "Configuração Geral do Site"