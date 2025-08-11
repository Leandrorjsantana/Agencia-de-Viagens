# offers/admin.py

from django.contrib import admin
from .models import Offer
from site_settings.models import SiteConfiguration
import random
import string

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_code', 'service', 'price', 'is_active', 'show_on_landing_page')
    list_filter = ('service', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('offer_code',)
    
    # --- CORREÇÃO ADICIONADA AQUI ---
    # Diz ao Django para permitir a busca por título, subtítulo ou código da oferta.
    search_fields = ('title', 'subtitle', 'offer_code')

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.offer_code:
            config = SiteConfiguration.objects.first()
            prefix = config.offer_code_prefix if config else 'OFR'
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            obj.offer_code = f"{prefix}-{random_part}"
        
        super().save_model(request, obj, form, change)