"""Django settings for compare project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os
import re
import socket
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir"
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="django-insecure-8^lf#k6(y&so=5b_@c7%bh4b4s9=z%cvmfmz20uem)ct2k-eri",
)

DEBUG = not any(
    [
        os.environ.get("RENDER"),
        os.environ.get("PRODUCTION"),
        os.environ.get("DJANGO_ENV") == "production",
    ]
)

ROOT_URLCONF = "compare.urls"

WSGI_APPLICATION = "compare.wsgi.application"

APPEND_SLASH = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Hosts & CORS
# ---------------------------------------------------------------------------


def get_server_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return None


server_ip = get_server_ip()

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    *(([server_ip]) if server_ip else []),
]

# Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Droplet
DROPLET_HOST = os.environ.get("ALLOWED_HOST")
if DROPLET_HOST:
    ALLOWED_HOSTS.append(DROPLET_HOST)
    ALLOWED_HOSTS.append(f"www.{DROPLET_HOST}")

CORS_ORIGIN_ALLOW_ALL = DEBUG

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
    r"^https?://onrender\.com$",
    r"^https?://compare-django\.onrender\.com$",
    r"^https?://compare-vue\.onrender\.com$",
    *(([rf"^https?://{re.escape(server_ip)}$"]) if server_ip else []),
    *(
        [
            rf"^https?://{re.escape(DROPLET_HOST)}$",
            rf"^https?://www\.{re.escape(DROPLET_HOST)}$",
        ]
        if DROPLET_HOST
        else []
    ),
]


# ---------------------------------------------------------------------------
# Apps & Middleware
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "graphene_django",
    # Local
    "tools",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


# ---------------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# Auth
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------------------------------
# Static files
# https://docs.djangoproject.com/en/stable/howto/static-files/
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


# ---------------------------------------------------------------------------
# Logging
# https://docs.djangoproject.com/en/stable/topics/logging/
# ---------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}


# ---------------------------------------------------------------------------
# Third-party: Graphene
# ---------------------------------------------------------------------------

GRAPHENE = {
    "SCHEMA": "compare.schema.schema",
    "SCHEMA_INDENT": 2,
    "MIDDLEWARE": ("graphene_django.debug.DjangoDebugMiddleware",),
}


# ---------------------------------------------------------------------------
# Third-party: django-graphene-filters
# ---------------------------------------------------------------------------

DJANGO_GRAPHENE_FILTERS = {
    "HIDE_FLAT_FILTERS": True,
}
