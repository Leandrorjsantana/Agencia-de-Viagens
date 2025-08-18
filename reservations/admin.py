# reservations/admin.py
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Reservation, ReservationDocument

class ReservationAdminForm(forms.ModelForm):
    # This form is now primarily for the ADD view, but will be used by the change view
    # where the fields are handled by readonly_fields.
    
    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # --- CORREÇÃO AQUI ---
        # Só tentamos customizar o campo 'client' se ele estiver no formulário.
        # (Ele não estará no formulário na tela de edição, pois é readonly).
        if 'client' in self.fields:
            self.fields['client'].label_from_instance = self.label_for_client

    def label_for_client(self, obj):
        if obj.get_full_name():
            return f"{obj.get_full_name()} ({obj.username})"
        return obj.username

class ReservationDocumentInline(admin.TabularInline):
    model = ReservationDocument
    fields = ('description', 'file', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_by', 'uploaded_at',)
    extra = 1

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    inlines = [ReservationDocumentInline]
    list_display = ('reservation_code', 'client', 'offer', 'start_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('reservation_code', 'client__username', 'client__first_name', 'offer__title', 'offer__offer_code')
    autocomplete_fields = ['client', 'offer']
    
    def offer_code_display(self, obj):
        if obj and obj.offer:
            return obj.offer.offer_code
        return "N/A"
    offer_code_display.short_description = "Código da Oferta"

    def get_readonly_fields(self, request, obj=None):
        # When obj is None, we are on the ADD page
        # When obj is not None, we are on the CHANGE page
        base_readonly = ('created_at', 'updated_at', 'offer_code_display')
        if obj: # On the CHANGE page, make these fields readonly
            return base_readonly + ('client', 'offer', 'reservation_code', 'start_date', 'end_date', 'total_price')
        return base_readonly # On the ADD page, these are editable (by our JS)

    fieldsets = (
        ("Dados Principais", {
            'fields': ('client', 'offer', 'status')
        }),
        ("Dados da Reserva (Gerado Automaticamente)", {
            'fields': ('offer_code_display', 'reservation_code', 'start_date', 'end_date', 'total_price')
        }),
        ("Outras Informações", {
            'fields': ('notes', 'has_been_reviewed', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and obj.offer: # Only on creation
            obj.total_price = obj.offer.price
            # The JS handles the other fields, but this is a server-side backup for price
        super().save_model(request, obj, form, change)

    class Media:
        js = ('core/js/admin_reservation_form.js',)