# offers/admin.py

from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'price', 'is_active', 'show_on_landing_page')
    list_filter = ('service', 'is_active')
    prepopulated_fields = {'slug': ('title',)}