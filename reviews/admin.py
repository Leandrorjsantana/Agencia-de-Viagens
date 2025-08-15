# reviews/admin.py
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'offer',
        'author',
        'rating',
        'is_approved',
        'is_featured',
        'created_at'
    )
    
    list_filter = ('is_approved', 'is_featured', 'rating', 'created_at')
    
    search_fields = ('title', 'content', 'author__username', 'offer__title')
    
    readonly_fields = ('created_at',)
    
    # ORGANIZANDO OS CAMPOS E ADICIONANDO 'photo'
    fieldsets = (
        ('Controle da Avaliação', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Detalhes da Avaliação', {
            'fields': ('offer', 'author', 'title', 'content', 'rating', 'photo', 'created_at')
        }),
    )

    list_per_page = 25