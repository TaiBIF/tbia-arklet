"""
Django settings for arklet project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set default values
    # ARKLET_HOST=(str, "127.0.0.1"),
    # ARKLET_DEBUG=(bool, False),
    # ARKLET_POSTGRES_NAME=(str, "arklet"),
    # ARKLET_POSTGRES_HOST=(str, "127.0.0.1"),
    # ARKLET_POSTGRES_PORT=(str, "5432"),
    # ARKLET_POSTGRES_USER=(str, "arklet"),
    # ARKLET_POSTGRES_PASSWORD=(str, "arklet"),
    # ARKLET_SENTRY_DSN=(str, ""),
    # ARKLET_SENTRY_TRANSACTIONS_PER_TRACE=(int, 1),
    # ARKLET_STATIC_ROOT=(str, "static"),
    # ARKLET_MEDIA_ROOT=(str, "media"),
    RESOLVER=(bool, False),
    # ARKLET_NOID_LENGTH=(int, 8)
)

# print(os.listdir(BASE_DIR))

# .env files are optional. django-environ will log an INFO message if no file is found
# and arklet will continue to run assuming all required environment variables are set.
env = environ.Env(DEBUG=(bool, False))
# print('BASE_DIR', BASE_DIR)
# env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("ARKLET_DJANGO_SECRET_KEY")  # Intentionally no default value

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("ARKLET_DEBUG")

ALLOWED_HOSTS = env.list("ARKLET_HOST")
for ah in ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS = [
        f"http://*.127.0.0.1",
        f"http://*.127.0.0.1:{env('ARKLET_PORT')}",
        f"http://*.{ah}",
        f"https://*.{ah}",
        f"http://*.{ah}:{env('ARKLET_PORT')}",
        f"https://*.{ah}:{env('ARKLET_PORT')}",
    ]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ark.apps.ArkConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "arklet.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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


WSGI_APPLICATION = "arklet.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("ARKLET_POSTGRES_NAME"),
        "HOST": env("ARKLET_POSTGRES_HOST"),
        "PORT": env("ARKLET_POSTGRES_PORT"),
        "USER": env("ARKLET_POSTGRES_USER"),
        "PASSWORD": env("ARKLET_POSTGRES_PASSWORD"),
        "DISABLE_SERVER_SIDE_CURSORS": True,  # required for pgbouncer transaction mode
    }
}


AUTH_USER_MODEL = "ark.User"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = env.str("ARKLET_STATIC_ROOT")

MEDIA_ROOT = env.str("ARKLET_MEDIA_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SENTRY_DSN = env("ARKLET_SENTRY_DSN")
SENTRY_SAMPLE_RATE = 1 / int(env("ARKLET_SENTRY_TRANSACTIONS_PER_TRACE"))
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=SENTRY_SAMPLE_RATE,
        send_default_pii=True,
    )
