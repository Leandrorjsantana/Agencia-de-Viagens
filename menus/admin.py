# menus/admin.py

from django.contrib import admin
from .models import TopBarLink, MenuItem, SocialMediaLink
# CORREÇÃO: O nome correto da biblioteca é 'adminsortable2'
from adminsortable2.admin import SortableAdminMixin

@admin.register(TopBarLink)
class TopBarLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'url')

@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'is_external')

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'url')