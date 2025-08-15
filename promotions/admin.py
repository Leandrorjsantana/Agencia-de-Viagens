# promotions/admin.py

from django.contrib import admin
from .models import PromotionCard
from adminsortable2.admin import SortableAdminMixin

@admin.register(PromotionCard)
class PromotionCardAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active')