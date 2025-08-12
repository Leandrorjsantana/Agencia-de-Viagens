# offers/admin.py

from django.contrib import admin
from .models import Offer
from site_settings.models import SiteConfiguration
import random
import string

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_code', 'destination_city', 'service', 'price', 'is_active')
    list_filter = ('service', 'is_active', 'destination_city')
    search_fields = ('title', 'subtitle', 'offer_code', 'destination_city')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('offer_code',)

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.offer_code:
            config = SiteConfiguration.objects.first()
            prefix = config.offer_code_prefix if config else 'OFR'
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            obj.offer_code = f"{prefix}-{random_part}"
        
        super().save_model(request, obj, form, change)