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
    search_fields = ('title', 'subtitle', 'offer_code')

    def save_model(self, request, obj, form, change):
        # Se for uma nova oferta e ainda não tiver um código
        if not obj.pk and not obj.offer_code:
            # Busca o prefixo nas configurações do site
            config = SiteConfiguration.objects.first()
            prefix = config.offer_code_prefix if config else 'OFR'
            
            # Gera uma parte aleatória para o código
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            obj.offer_code = f"{prefix}-{random_part}"
        
        super().save_model(request, obj, form, change)