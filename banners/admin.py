# banners/admin.py

from django.contrib import admin
from .models import Banner
from adminsortable2.admin import SortableAdminMixin

@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active')