# leads/admin.py

from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # O Django é inteligente e já vai usar os novos nomes do modelo,
    # mas este código garante que a exibição fique perfeita.
    list_display = ('full_name', 'offer', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'offer')
    search_fields = ('full_name', 'email', 'offer__title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Status da Solicitação', {
            'fields': ('status',)
        }),
        ('Oferta de Interesse', {
            'fields': ('offer',)
        }),
        ('Dados do Cliente', {
            'fields': ('full_name', 'email', 'phone_number', 'client_user')
        }),
        ('Detalhes da Viagem', {
            'fields': ('travel_date', 'number_of_people', 'observations')
        }),
        ('Datas', {
            'fields': ('created_at',)
        }),
    )

    def has_add_permission(self, request):
        return False