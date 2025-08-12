# contacts/admin.py

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'status', 'received_at')
    list_filter = ('status', 'received_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'message', 'received_at')
    
    fieldsets = (
        (None, {
            'fields': ('status',)
        }),
        ('Detalhes da Mensagem', {
            'fields': ('full_name', 'email', 'phone', 'subject', 'message', 'received_at')
        }),
    )

    def has_add_permission(self, request):
        return False