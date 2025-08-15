# help_center/admin.py

from django.contrib import admin
from .models import HelpCategory, HelpArticle
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin

class HelpArticleInline(SortableInlineAdminMixin, admin.TabularInline):
    model = HelpArticle
    extra = 1
    fields = ('question', 'answer')

@admin.register(HelpCategory)
class HelpCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HelpArticleInline]