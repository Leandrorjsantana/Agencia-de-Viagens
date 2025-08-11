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
            'fields': ('public_email', 'public_whatsapp')
        }),
        ('Configurações de Códigos', {
            'fields': ('offer_code_prefix',)
        }),
        ('Estilo Global', {
            'fields': ('main_font', 'primary_color')
        }),
        ('Cores Detalhadas', {
            'classes': ('collapse',),
            'fields': (('top_bar_bg_color', 'top_bar_text_color'), ('main_header_bg_color', 'main_header_text_color'), ('footer_bg_color', 'footer_text_color'))
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