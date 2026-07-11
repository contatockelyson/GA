"""
Django settings for config project.
Preparado para desenvolvimento local e deploy no Render.
"""

import os
from pathlib import Path

import dj_database_url


# =========================================================
# CAMINHOS DO PROJETO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SEGURANÇA
# =========================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-chave-apenas-para-desenvolvimento-local",
)

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]

# Permite adicionar o domínio específico pelo Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# Permite adicionar domínio personalizado
CUSTOM_DOMAIN = os.environ.get("CUSTOM_DOMAIN")

if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)
    CSRF_TRUSTED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")


# =========================================================
# APLICAÇÕES
# =========================================================

INSTALLED_APPS = [
    "operacoes",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# =========================================================
# MIDDLEWARES
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Responsável por servir os arquivos estáticos no Render
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS E WSGI
# =========================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Permite templates em uma pasta geral chamada templates
        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# BANCO DE DADOS
# =========================================================

# No Render, será utilizada a variável DATABASE_URL.
# Localmente, caso DATABASE_URL não exista, será usado SQLite.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cim',
        'USER': 'admin',
        'PASSWORD': 'SUA_SENHA',
        'HOST': 'dpg-d8rb58j7uimc73evgji0-a.ohio-postgres.render.com',
        'PORT': '5432',
    }
}


# =========================================================
# VALIDAÇÃO DE SENHAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNACIONALIZAÇÃO
# =========================================================

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Fortaleza"

USE_I18N = True

USE_TZ = True


# =========================================================
# ARQUIVOS ESTÁTICOS
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Use esta pasta para seus arquivos CSS, JS e imagens gerais.
# Crie a pasta static na raiz do projeto.
STATICFILES_DIRS = []

if (BASE_DIR / "static").exists():
    STATICFILES_DIRS.append(BASE_DIR / "static")


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# =========================================================
# ARQUIVOS DE MÍDIA
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# CONFIGURAÇÕES PADRÃO
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# CONFIGURAÇÕES DO SISTEMA
# =========================================================

SENHA_EXCLUSAO = os.environ.get(
    "SENHA_EXCLUSAO",
    "1234",
)


# =========================================================
# SEGURANÇA EM PRODUÇÃO
# =========================================================

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )