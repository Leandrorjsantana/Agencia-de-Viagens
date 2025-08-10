from django.contrib import admin

# Register your models here.
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define um formulário "embutido" para o Perfil
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil do Cliente'
    fk_name = 'user'

# Define uma nova classe de Admin para o Usuário
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Desregistra o UserAdmin padrão do Django
admin.site.unregister(User)
# Registra o User novamente com a nossa configuração customizada
admin.site.register(User, CustomUserAdmin)