# reviews/admin.py
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'offer', 'rating', 'is_approved', 'is_featured', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'rating')
    search_fields = ('title', 'content', 'author__username', 'offer__title')
    autocomplete_fields = ['author', 'offer']

    # Adicionando o novo campo de foto ao formulário
    fields = ('author', 'offer', 'title', 'content', 'rating', 'photo', 'is_approved', 'is_featured')