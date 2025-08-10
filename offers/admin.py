# offers/admin.py

from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    # Agora o Django vai encontrar os campos 'service' e 'price' sem problemas.
    list_display = ('title', 'service', 'price', 'is_active', 'show_on_landing_page')
    list_filter = ('service', 'is_active')
    search_fields = ('title', 'subtitle', 'service__name')
    prepopulated_fields = {'slug': ('title',)}