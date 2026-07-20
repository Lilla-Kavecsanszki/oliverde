"""
Django settings for the Oliverde project.

Django 6.0.7.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# -------------------------------------------------------------------
# Paths and environment variables
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# -------------------------------------------------------------------
# Core settings
# -------------------------------------------------------------------

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]


# -------------------------------------------------------------------
# Applications
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Third-party applications
    "django_ckeditor_5",
    "cloudinary_storage",
    "cloudinary",

    # Oliverde applications
    "accounts",
    "core",
    "portfolio",
    "services",
    "journal",
]


# -------------------------------------------------------------------
# CKEditor 5
# -------------------------------------------------------------------

CKEDITOR_5_UPLOAD_PATH = "journal/uploads/"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "insertImage",
            "|",
            "undo",
            "redo",
        ],
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ],
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignCenter",
                "imageStyle:alignRight",
            ],
            "styles": [
                "alignLeft",
                "alignCenter",
                "alignRight",
            ],
        },
        "link": {
            "addTargetToExternalLinks": True,
            "defaultProtocol": "https://",
        },
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"


# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -------------------------------------------------------------------
# URL and template configuration
# -------------------------------------------------------------------

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.nav_destinations",
                "core.context_processors.site_url",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}


# -------------------------------------------------------------------
# Authentication
# -------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

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


# -------------------------------------------------------------------
# Internationalisation
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Rome"

USE_I18N = True

USE_TZ = True


# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# -------------------------------------------------------------------
# Cloudinary media storage
# -------------------------------------------------------------------

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ["CLOUDINARY_CLOUD_NAME"],
    "API_KEY": os.environ["CLOUDINARY_API_KEY"],
    "API_SECRET": os.environ["CLOUDINARY_API_SECRET"],
    "SECURE": True,
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}

MEDIA_URL = "/media/"


# -------------------------------------------------------------------
# Default primary key
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -------------------------------------------------------------------
# Security
# -------------------------------------------------------------------

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

if not DEBUG:
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_HSTS_SECONDS = int(
        os.environ.get(
            "SECURE_HSTS_SECONDS",
            "0",
        )
    )

    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        SECURE_HSTS_SECONDS > 0
    )

    SECURE_HSTS_PRELOAD = False


# -------------------------------------------------------------------
# Site URL
# -------------------------------------------------------------------

SITE_URL = os.environ.get(
    "SITE_URL",
    "https://oliverdepropertymanagement.com",
)