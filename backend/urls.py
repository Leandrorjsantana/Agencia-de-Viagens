# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # --- NOSSAS ROTAS DE API V1 ---
    path('api/v1/', include('core.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/reservations/', include('reservations.urls')),
    path('api/v1/offers/', include('offers.urls')),
    path('api/v1/subscribers/', include('subscribers.urls')),
    
    # --- CORREÇÃO ADICIONADA AQUI: Conectando as rotas do nosso app 'contacts' ---
    path('api/v1/contacts/', include('contacts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)