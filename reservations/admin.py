# reservations/admin.py

from django.contrib import admin
from django import forms
from .models import Reservation, ReservationDocument

class ReservationAdminForm(forms.ModelForm):
    # Campo para confirmação do nome do cliente
    client_name_confirmation = forms.CharField(
        label="Nome do Cliente (Confirmação)", 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background: #f0f0f0; border: none;'})
    )
    
    # Novo campo para exibir o Código da Oferta
    offer_code_placeholder = forms.CharField(
        label="Código da Oferta",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background: #f0f0f0; border: none;'})
    )

    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationDocumentInline(admin.TabularInline):
    model = ReservationDocument
    fields = ('description', 'file', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_by', 'uploaded_at',)
    extra = 1

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    inlines = [ReservationDocumentInline]
    list_display = ('reservation_code', 'client_full_name_display', 'offer', 'start_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('reservation_code', 'client__username', 'client__first_name', 'client__last_name', 'offer__title', 'offer__offer_code')
    autocomplete_fields = ['client', 'offer']
    
    def client_full_name_display(self, obj):
        if obj.client:
            return obj.client.get_full_name() or obj.client.username
        return "N/A"
    client_full_name_display.short_description = 'Cliente'
    client_full_name_display.admin_order_field = 'client__first_name'

    def get_readonly_fields(self, request, obj=None):
        if obj: # Editando
            return ('created_at', 'updated_at', 'client', 'offer', 'reservation_code', 'start_date', 'end_date', 'total_price')
        return ('created_at', 'updated_at') # Criando

    fieldsets = (
        ("Dados Principais", {
            'fields': ('client', 'client_name_confirmation', 'offer', 'status')
        }),
        ("Dados da Reserva (Gerado Automaticamente)", {
            'fields': ('offer_code_placeholder', 'reservation_code', 'start_date', 'end_date', 'total_price')
        }),
        ("Outras Informações", {
            'fields': ('notes', 'has_been_reviewed', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and obj.offer:
            obj.total_price = obj.offer.price
        super().save_model(request, obj, form, change)

    class Media:
        js = ('core/js/admin_reservation_form.js',)