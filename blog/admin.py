# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Tag, BlogAdBanner, Comment
from adminsortable2.admin import SortableAdminMixin

# --- NOVA SECÇÃO PARA MODERAÇÃO DE COMENTÁRIOS ---
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'content', 'is_approved', 'created_at')
    readonly_fields = ('author', 'content', 'created_at')
    verbose_name = "Comentário"
    verbose_name_plural = "Moderação de Comentários"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_pinned', 'published_at')
    list_filter = ('is_published', 'category', 'tags')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['tags', 'category']
    # Adiciona a secção de comentários à página do post
    inlines = [CommentInline]
    
    fieldsets = (
        ('Conteúdo Principal', {
            'fields': ('title', 'slug', 'featured_image', 'summary', 'content')
        }),
        ('Organização', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Publicação', {
            'fields': ('is_published', 'is_pinned')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(BlogAdBanner)
class BlogAdBannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'is_active')