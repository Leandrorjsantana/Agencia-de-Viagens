# menus/admin.py

from django.contrib import admin
from .models import TopBarLink, MenuItem

# Estes comandos registram os dois modelos de menu no painel de administração.
admin.site.register(TopBarLink)
admin.site.register(MenuItem)