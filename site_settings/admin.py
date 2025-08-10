# site_settings/admin.py

from django.contrib import admin
from .models import SiteConfiguration

# Este comando registra o modelo SiteConfiguration no painel de administração.
admin.site.register(SiteConfiguration)