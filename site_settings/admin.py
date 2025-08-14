# site_settings/admin.py

from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidade Visual', {
            'fields': ('site_name', 'logo', 'logo_height', 'favicon')
        }),
        ('Informações de Contato Públicas', {
            'fields': ('public_email', 'public_whatsapp', 'address_street', 'address_neighborhood', ('address_city', 'address_state'), 'address_cep', 'opening_hours')
        }),
        ('Página de Contato', {
            'fields': ('contact_page_title', 'contact_page_subtitle', 'google_maps_embed_url', 'contact_form_subjects')
        }),
        ('Página Quem Somos', {
            'classes': ('collapse',),
            'fields': (
                'about_us_header_image', 'about_us_history', 
                'about_us_mission', 'about_us_vision', 'about_us_values',
                ('stat_years', 'stat_destinations', 'stat_clients')
            )
        }),
        ('Configurações de Códigos', {
            'fields': ('offer_code_prefix',)
        }),
        ('Estilo Global', {
            'fields': ('main_font', 'primary_color', 'page_header_bg_color') # <-- Adicionado aqui
        }),
        ('Seção de Busca (Hero)', {
            'fields': ('hero_background_color', 'hero_background_image', 'booking_form_bg_color')
        }),
        ('Seção de Newsletter', {
            'fields': ('newsletter_headline', 'newsletter_subheadline', 'newsletter_button_text', 'newsletter_background_color', 'newsletter_background_image')
        }),
        ('Configurações dos Carrosséis', {
            'fields': ('banner_autoplay_speed', 'offer_carousel_speed')
        }),
        ('Cores Detalhadas', {
            'classes': ('collapse',),
            'fields': (
                ('top_bar_bg_color', 'top_bar_text_color'), 
                ('main_header_bg_color', 'main_header_text_color'), 
                ('footer_bg_color', 'footer_text_color'),
            )
        }),
        ('Rodapé', {
            'fields': ('footer_text',)
        }),
        ('SEO e Scripts', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_description', 'tracking_header_scripts', 'tracking_body_start_scripts', 'tracking_body_end_scripts')
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False