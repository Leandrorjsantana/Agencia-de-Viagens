# site_settings/models.py

from django.db import models
from colorfield.fields import ColorField

class SiteConfiguration(models.Model):
    # Secção de Identidade Visual
    site_name = models.CharField(max_length=255, default='Agência de Viagens', verbose_name="Nome do Site")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Dimensão recomendada: 250x80 pixels")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text="Ícone quadrado. Dimensão recomendada: 64x64 pixels.", verbose_name="Favicon do Site")
    logo_height = models.PositiveIntegerField(default=50, help_text="Altura do logo em pixels (ex: 50).", verbose_name="Altura do Logo (em pixels)")

    # --- NOVOS CAMPOS DE CONTATO PÚBLICO ---
    public_email = models.EmailField(blank=True, verbose_name="E-mail Público de Contato")
    public_whatsapp = models.CharField(
        max_length=20, blank=True, 
        verbose_name="WhatsApp Público de Contato",
        help_text="Use o formato internacional, ex: 5511999999999"
    )

    # --- NOVO CAMPO PARA O PREFIXO ---
    offer_code_prefix = models.CharField(
        max_length=5, default='OFR',
        verbose_name="Prefixo do Código da Oferta",
        help_text="As 3 a 5 letras que irão no início de cada código de oferta (ex: RMV)."
    )

    # ... (outros campos existentes)
    main_font = models.CharField(max_length=100, default='Poppins', verbose_name="Fonte Principal")
    primary_color = ColorField(default='#0d6efd', verbose_name="Cor Primária (Botões e Links)")
    # ... (outros campos de cor)
    top_bar_bg_color = ColorField(default='#F8F9FA', verbose_name="Fundo da Barra Superior")
    top_bar_text_color = ColorField(default='#6C757D', verbose_name="Texto da Barra Superior")
    main_header_bg_color = ColorField(default='#FFFFFF', verbose_name="Fundo do Cabeçalho Principal")
    main_header_text_color = ColorField(default='#333333', verbose_name="Texto do Cabeçalho Principal")
    footer_bg_color = ColorField(default='#212529', verbose_name="Fundo do Rodapé")
    footer_text_color = ColorField(default='#FFFFFF', verbose_name="Texto do Rodapé")
    footer_text = models.TextField(blank=True, verbose_name="Texto do Rodapé")
    # ... (campos de SEO e Scripts)
    seo_title = models.CharField(max_length=60, blank=True, verbose_name="Título para o Google")
    seo_description = models.TextField(max_length=160, blank=True, verbose_name="Descrição para o Google")
    tracking_header_scripts = models.TextField(blank=True, verbose_name="Scripts no Cabeçalho (<head>)")
    tracking_body_start_scripts = models.TextField(blank=True, verbose_name="Scripts no Início do Corpo (<body>)")
    tracking_body_end_scripts = models.TextField(blank=True, verbose_name="Scripts no Fim do Corpo (</body>)")


    def __str__(self):
        return "Configurações Gerais do Site"

    class Meta:
        verbose_name = "Configuração Geral do Site"