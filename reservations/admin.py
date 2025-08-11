# reservations/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation, ReservationDocument

class AdminDocumentInline(admin.TabularInline):
    model = ReservationDocument
    extra = 1
    verbose_name = "Documento Enviado pelo Admin"
    verbose_name_plural = "Documentos Enviados pelo Admin"
    fields = ('description', 'file', 'view_document_link', 'uploaded_at')
    readonly_fields = ('view_document_link', 'uploaded_at')

    def view_document_link(self, obj):
        if obj.file:
            # Adicionamos a classe "button-link" ao nosso link
            return format_html('<a href="{}" target="_blank" class="button-link">Ver Documento</a>', obj.file.url)
        return "Nenhum arquivo"
    view_document_link.short_description = "Ver"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(uploaded_by='ADMIN')

class ClientDocumentInline(admin.TabularInline):
    model = ReservationDocument
    extra = 0
    can_delete = False
    verbose_name = "Documento Enviado pelo Cliente"
    verbose_name_plural = "Documentos Enviados pelo Cliente"
    fields = ('description', 'file', 'view_document_link', 'uploaded_at')
    readonly_fields = ('description', 'file', 'view_document_link', 'uploaded_at')

    def view_document_link(self, obj):
        if obj.file:
            # Adicionamos as classes "button-link" e "view-only" ao link
            return format_html('<a href="{}" target="_blank" class="button-link view-only">Ver Comprovante</a>', obj.file.url)
        return "Nenhum arquivo"
    view_document_link.short_description = "Ver"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(uploaded_by='CLIENT')

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_code', 'client', 'offer', 'start_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('reservation_code', 'client__username', 'client__profile__full_name', 'offer__title')
    inlines = [AdminDocumentInline, ClientDocumentInline]
    autocomplete_fields = ['client', 'offer']

    # Esta classe diz ao Django para carregar nosso arquivo de CSS customizado
    # sempre que esta página do admin for aberta.
    class Media:
        css = {
            'all': ('core/css/admin_custom.css',)
        }