import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY and DEBUG from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
DEBUG = int(os.environ.get("DEBUG", default=0))

# Hosts configuration
# Alterações realizadas em 23/10/2024 para testes
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")
ALLOWED_HOSTS = ['localhost','127.0.0.1', 'ebac-livraria-api.herokuapp.com']


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",  # Admin app
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",  # Sessions for admin and other functionalities
    "django.contrib.messages",  # MessageMiddleware depends on this app
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "order",
    "product",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Reforça configurações de segurança
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Gerenciamento de arquivos estáticos
    "django.contrib.sessions.middleware.SessionMiddleware",  # Habilita o uso de sessões
    "django.middleware.common.CommonMiddleware",  # Middleware comum para várias funcionalidades
    "django.middleware.csrf.CsrfViewMiddleware",  # Proteção contra CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Gerencia a autenticação do usuário
    "django.contrib.messages.middleware.MessageMiddleware",  # Gerencia mensagens no sistema
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protege contra ataques de clickjacking
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Django Debug Toolbar
]

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Add additional template directories if needed
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookstore.wsgi.application"

STATIC_ROOT = BASE_DIR / 'staticfiles' # Diretório onde todos os arquivos estáticos serão coletados pelo comando 'collectstatic'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Database configuration, using environment variables
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = ["127.0.0.1"]

# Django REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
