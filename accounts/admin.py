# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from reservations.models import Reservation

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    show_change_link = True
    fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')
    readonly_fields = ('reservation_code', 'offer', 'start_date', 'status', 'total_price')
    def has_add_permission(self, request, obj=None):
        return False

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil do Cliente'
    fk_name = 'user'
    # Adicionando o novo campo de foto de perfil
    fields = ('profile_picture', 'full_name', 'cpf', 'phone_number', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado')

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, ReservationInline)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)