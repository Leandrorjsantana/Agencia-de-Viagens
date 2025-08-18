# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from reservations.models import Reservation

# Seu inline de Reservas (mantido como está)
class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    show_change_link = True
    fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')
    readonly_fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')
    def has_add_permission(self, request, obj=None):
        return False

# Seu inline de Perfil (mantido como está)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil do Cliente'
    fk_name = 'user'
    fields = ('profile_picture', 'full_name', 'cpf', 'phone_number', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado')

# Nosso admin de Usuário customizado com as correções
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, ReservationInline)
    
    # --- AJUSTE 1: MELHORA A VISUALIZAÇÃO DA LISTA DE USUÁRIOS ---
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # --- AJUSTE 2 (A CORREÇÃO PRINCIPAL): DEFINE OS CAMPOS DE BUSCA ---
    # Esta linha instrui o 'autocomplete_fields' a pesquisar nestes campos
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Desregistra o admin padrão
admin.site.unregister(User)
# Registra o seu admin customizado
admin.site.register(User, CustomUserAdmin)