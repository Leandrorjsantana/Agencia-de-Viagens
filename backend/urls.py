# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- NOSSAS ROTAS DE API ---
    path('api/v1/', include('core.urls')),
    # Futuramente, adicionaremos as rotas de autenticação aqui também
]

# Permite que o Django sirva os arquivos de imagem que você sobe no admin
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)