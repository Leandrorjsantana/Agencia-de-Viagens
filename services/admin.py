# services/admin.py

from django.contrib import admin
from .models import Service
from adminsortable2.admin import SortableAdminMixin

@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

    # Deixa o campo JSON um pouco maior e mais fácil de editar
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }