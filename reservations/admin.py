# reservations/admin.py

from django.contrib import admin
from .models import Reservation, ReservationDocument

class ReservationDocumentInline(admin.TabularInline):
    model = ReservationDocument
    extra = 1 # Começa com 1 campo de upload de arquivo

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_code', 'client', 'offer', 'start_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('reservation_code', 'client__username', 'client__profile__full_name', 'offer__title')
    inlines = [ReservationDocumentInline]
    autocomplete_fields = ['client', 'offer'] # Adiciona uma busca inteligente para Cliente e Oferta