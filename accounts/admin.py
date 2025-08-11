# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from reservations.models import Reservation # Importa o modelo de Reserva

# Define um formulário "embutido" para as Reservas, no formato de tabela
class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0 # Não mostra formulários de reserva em branco por padrão
    show_change_link = True # Adiciona um link para editar a reserva completa
    
    # Define os campos que aparecerão na tabela
    fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')
    # Torna os campos apenas leitura, pois a edição deve ser feita na área de Reservas
    readonly_fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')

    # Impede a criação de novas reservas a partir da tela do usuário
    def has_add_permission(self, request, obj=None):
        return False

# Define um formulário "embutido" para o Perfil
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil do Cliente'
    fk_name = 'user'

# Define a nossa nova classe de Admin para o Usuário
class CustomUserAdmin(BaseUserAdmin):
    # Adiciona os formulários embutidos de Perfil e Reservas
    inlines = (ProfileInline, ReservationInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Desregistra o UserAdmin padrão do Django
admin.site.unregister(User)
# Registra o User novamente com a nossa configuração customizada
admin.site.register(User, CustomUserAdmin)