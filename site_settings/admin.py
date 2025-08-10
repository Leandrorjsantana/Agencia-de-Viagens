# site_settings/admin.py

from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidade Visual', {
            'fields': ('site_name', 'logo', 'logo_height', 'favicon')
        }),
        ('Estilo Global', {
            'fields': ('main_font', 'primary_color')
        }),
        ('Seção de Busca (Hero)', {
            'fields': ('hero_background_color', 'hero_background_image')
        }),
        # NOVO: Seção para os Carrosséis
        ('Configurações dos Carrosséis', {
            'fields': ('banner_autoplay_speed', 'offer_carousel_speed')
        }),
        ('Seção de Newsletter', {
            'fields': ('newsletter_headline', 'newsletter_subheadline', 'newsletter_button_text', 'newsletter_background_color', 'newsletter_background_image')
        }),
        ('Cores Detalhadas', {
            'classes': ('collapse',),
            'fields': (('top_bar_bg_color', 'top_bar_text_color'), ('main_header_bg_color', 'main_header_text_color'), ('footer_bg_color', 'footer_text_color'))
        }),
        ('SEO e Metatags', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_description')
        }),
        ('Scripts de Rastreamento (Marketing)', {
            'classes': ('collapse',),
            'fields': ('tracking_header_scripts', 'tracking_body_start_scripts', 'tracking_body_end_scripts')
        }),
        ('Rodapé', {
            'fields': ('footer_text',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False