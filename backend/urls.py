# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- NOSSAS ROTAS DE API V1 ---
    path('api/v1/', include('core.urls')),
    
    # Adicionando as rotas de autenticação (login, etc.) que usaremos no futuro
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Conectando as rotas do nosso app 'accounts' (que contém o /register/)
    path('api/v1/accounts/', include('accounts.urls')),
]

# Permite que o Django sirva os arquivos de imagem que você sobe no admin
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)