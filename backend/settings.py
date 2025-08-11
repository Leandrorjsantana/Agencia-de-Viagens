# backend/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-seu-segredo-aqui-vamos-mudar-depois'
DEBUG = True
ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'corsheaders',
    'colorfield',
    'adminsortable2',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'site_settings.apps.SiteSettingsConfig',
    'menus.apps.MenusConfig',
    'pages.apps.PagesConfig',
    'services.apps.ServicesConfig',
    'offers.apps.OffersConfig',
    'blog.apps.BlogConfig',
    'banners.apps.BannersConfig',
    'reservations.apps.ReservationsConfig',
    'subscribers.apps.SubscribersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# --- CORREÇÃO AQUI: Removendo a formatação de link inválida ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

REST_AUTH = {
    'USE_JWT': True,
    'LOGIN_SERIALIZER': 'accounts.serializers.CustomLoginSerializer',
    'REGISTER_SERIALIZER': 'accounts.serializers.RegisterSerializer',
}

JAZZMIN_SETTINGS = {
    "site_title": "Painel da Agência",
    "site_header": "Agência de Viagens",
    "site_brand": "Painel Administrativo",
    "welcome_sign": "Bem-vindo ao painel de controlo da sua agência",
    "copyright": "Sua Agência de Viagens",
    "show_ui_builder": True,
    "order_with_respect_to": [
        "site_settings", "banners", "menus",
        "services", "offers", "reservations",
        "subscribers", "blog",
        "auth", "accounts",
    ],
    "apps": {
        "site_settings": {"name": "Configurações do Site", "icon": "fa fa-cog"},
        "banners": {"name": "Gestão da Página Inicial", "icon": "fa fa-images"},
        "menus": {"name": "Gestão de Menus", "icon": "fa fa-bars"},
        "services": {"name": "Catálogo", "icon": "fa fa-concierge-bell"},
        "offers": {"name": "Catálogo", "icon": "fa fa-tag"},
        "reservations": {"name": "Vendas", "icon": "fa fa-file-invoice-dollar"},
        "subscribers": {"name": "Marketing", "icon": "fa fa-envelope"},
        "blog": {"name": "Marketing", "icon": "fa fa-rss"},
        "accounts": {"name": "Administração", "icon": "fa fa-users-cog"},
        "auth": {"name": "Administração", "icon": "fa fa-users"},
    },
    "icons": {
        "auth.User": "fa fa-user",
        "auth.Group": "fa fa-users",
        "accounts.profile": "fa fa-id-card",
        "banners.banner": "fa fa-image",
        "menus.topbarlink": "fa fa-arrow-up",
        "menus.menuitem": "fa fa-bars",
        "menus.socialmedialink": "fa fa-share-alt",
        "offers.offer": "fa fa-tags",
        "reservations.reservation": "fa fa-file-signature",
        "reservations.reservationdocument": "fa fa-file-alt",
        "services.service": "fa fa-concierge-bell",
        "site_settings.siteconfiguration": "fa fa-cogs",
        "subscribers.subscriber": "fa fa-at",
    },
    "hide_apps": ["authtoken", "account", "socialaccount"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
}