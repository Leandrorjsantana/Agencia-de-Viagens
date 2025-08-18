# site_settings/models.py

from django.db import models
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField

class SiteConfiguration(models.Model):
    # --- DADOS GERAIS E DE CONTATO ---
    site_name = models.CharField(max_length=255, default='Agência de Viagens', verbose_name="Nome do Site")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Dimensão recomendada: 250x80 pixels")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text="Ícone quadrado. Dimensão recomendada: 64x64 pixels.", verbose_name="Favicon do Site")
    logo_height = models.PositiveIntegerField(default=50, help_text="Altura do logo em pixels (ex: 50).", verbose_name="Altura do Logo (em pixels)")
    public_email = models.EmailField(blank=True, verbose_name="E-mail Público de Contato")
    public_whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp Público de Contato", help_text="Use o formato internacional, ex: 5511999999999")
    opening_hours = models.TextField(blank=True, verbose_name="Horário de Funcionamento", help_text="Use uma linha para cada dia. Ex: Seg - Sex: 09:00 - 18:00")
    
    # --- ENDEREÇO ---
    address_street = models.CharField(max_length=255, blank=True, verbose_name="Rua e Número")
    address_neighborhood = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    address_city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    address_state = models.CharField(max_length=50, blank=True, verbose_name="Estado")
    address_cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    google_maps_embed_url = models.URLField(max_length=500, blank=True, verbose_name="URL de Incorporação do Google Maps")

    # --- PÁGINA DE CONTATO ---
    contact_page_title = models.CharField(max_length=100, blank=True, default="Entre em Contato", verbose_name="Título da Página de Contato")
    contact_page_subtitle = models.CharField(max_length=255, blank=True, default="Será um prazer atendê-lo!", verbose_name="Subtítulo da Página de Contato")
    contact_form_subjects = models.TextField(blank=True, default="Dúvidas Gerais\nOrçamentos\nReclamações\nElogios", verbose_name="Assuntos do Formulário de Contato", help_text="Digite um assunto por linha.")

    # --- PÁGINA DE TELEVENDAS (COM TRADUÇÃO) ---
    televendas_phone = models.CharField(
        max_length=20, blank=True, 
        verbose_name="Telefone de Televendas",
        help_text="Número principal para ligações diretas. Ex: (11) 4002-8922"
    )
    televendas_page_title = models.CharField(max_length=100, blank=True, default="Fale com nossa equipe de Televendas", verbose_name="Título da Página de Televendas")
    televendas_page_subtitle = models.CharField(max_length=255, blank=True, default="Estamos prontos para o ajudar a reservar a sua viagem e a tirar todas as dúvidas.", verbose_name="Subtítulo da Página de Televendas")
    televendas_benefits = RichTextUploadingField(
        blank=True, 
        verbose_name="Benefícios / Informações Extras",
        help_text="Use listas ou parágrafos para destacar os benefícios do seu atendimento."
    )

    # --- PÁGINA 'QUEM SOMOS' ---
    about_us_header_image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name="Imagem de Cabeçalho (Quem Somos)", help_text="Imagem de abertura da página. Dimensão recomendada: 1920x500 pixels.")
    about_us_history = RichTextUploadingField(blank=True, verbose_name="História da Agência")
    about_us_mission = models.TextField(blank=True, verbose_name="Nossa Missão")
    about_us_vision = models.TextField(blank=True, verbose_name="Nossa Visão")
    about_us_values = models.TextField(blank=True, verbose_name="Nossos Valores (um por linha)")
    stat_years = models.CharField(max_length=10, default="10+", verbose_name="Anos no Mercado")
    stat_destinations = models.CharField(max_length=10, default="500+", verbose_name="Destinos Atendidos")
    stat_clients = models.CharField(max_length=10, default="10.000+", verbose_name="Clientes Felizes")

    # --- PÁGINA DE EXPERIÊNCIAS / AVALIAÇÕES ---
    experiences_page_title = models.CharField(max_length=100, blank=True, default="O que nossos viajantes dizem", verbose_name="Título da Página de Experiências")
    experiences_page_subtitle = models.CharField(max_length=255, blank=True, default="Histórias reais que inspiram novas viagens.", verbose_name="Subtítulo da Página de Experiências")

    # --- CONFIGURAÇÕES GLOBAIS E DE ESTILO ---
    offer_code_prefix = models.CharField(max_length=5, default='OFR', verbose_name="Prefixo do Código da Oferta")
    hero_background_color = ColorField(default='#333333', verbose_name="Cor de Fundo da Seção de Busca")
    hero_background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text="Opcional. Dimensão recomendada: 1920x500 pixels.", verbose_name="Imagem de Fundo da Seção de Busca")
    booking_form_bg_color = ColorField(default='#FFFFFF', verbose_name="Cor de Fundo do Formulário de Busca")
    newsletter_headline = models.CharField(max_length=100, blank=True, verbose_name="Título da Newsletter")
    newsletter_subheadline = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo da Newsletter")
    newsletter_button_text = models.CharField(max_length=50, default='Inscrever-se', verbose_name="Texto do Botão da Newsletter")
    newsletter_background_color = ColorField(default='#212529', verbose_name="Cor de Fundo da Newsletter")
    newsletter_background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text="Opcional. Dimensão recomendada: 1920x400 pixels.", verbose_name="Imagem de Fundo da Newsletter")
    banner_autoplay_speed = models.PositiveIntegerField(default=5000, help_text="Velocidade em milissegundos (ex: 5000 para 5 segundos). Digite 0 para desativar.", verbose_name="Velocidade do Carrossel de Banners (ms)")
    offer_carousel_speed = models.PositiveIntegerField(default=0, help_text="Velocidade em milissegundos (ex: 4000 para 4 segundos). Digite 0 para desativar.", verbose_name="Velocidade do Carrossel de Ofertas (ms)")
    main_font = models.CharField(max_length=100, default='Poppins', verbose_name="Fonte Principal")
    primary_color = ColorField(default='#0d6efd', verbose_name="Cor Primária (Botões e Links)")
    page_header_bg_color = ColorField(default='#003366', verbose_name="Cor de Fundo Padrão dos Cabeçalhos de Página")
    top_bar_bg_color = ColorField(default='#F8F9FA', verbose_name="Fundo da Barra Superior")
    top_bar_text_color = ColorField(default='#6C757D', verbose_name="Texto da Barra Superior")
    main_header_bg_color = ColorField(default='#FFFFFF', verbose_name="Fundo do Cabeçalho Principal")
    main_header_text_color = ColorField(default='#333333', verbose_name="Texto do Cabeçalho Principal")
    footer_bg_color = ColorField(default='#212529', verbose_name="Fundo do Rodapé")
    footer_text_color = ColorField(default='#FFFFFF', verbose_name="Texto do Rodapé")
    footer_text = models.TextField(blank=True, verbose_name="Texto do Rodapé")
    
    # --- SEO E SCRIPTS DE RASTREAMENTO ---
    seo_title = models.CharField(max_length=60, blank=True, verbose_name="Título para o Google")
    seo_description = models.TextField(max_length=160, blank=True, verbose_name="Descrição para o Google")
    tracking_header_scripts = models.TextField(blank=True, verbose_name="Scripts no Cabeçalho (<head>)")
    tracking_body_start_scripts = models.TextField(blank=True, verbose_name="Scripts no Início do Corpo (<body>)")
    tracking_body_end_scripts = models.TextField(blank=True, verbose_name="Scripts no Fim do Corpo (</body>)")

    def __str__(self):
        return "Configurações Gerais do Site"

    class Meta:
        verbose_name = "Configuração Geral do Site"