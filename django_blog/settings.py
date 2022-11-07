"""
Django settings for django_blog project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.template.context_processors import media

# Add custom languages not provided by Django
from django.conf import locale, global_settings
from django.utils.translation import gettext_lazy as _

from django_blog.productions import production_debug, production_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = production_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = production_debug

ALLOWED_HOSTS = ["*"] if DEBUG else ['https://adamspierredavid.com', 'www.adamspierredavid.com', 'adamspierredavid.com',
                                     '144.217.7.48']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'blog.apps.BlogConfig',
    'ckeditor',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ADDITIONAL CONFIGURATION STARTS HERE

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LAST_SEEN_TIMEOUT = 60 * 60 * 24 * 7

# Caches settings
CACHES_LOCATION = os.path.join(BASE_DIR, '.cache') if DEBUG else "/home/debian/.cache/WHERE_YOU_HOSTED_YOUR_BLOG"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHES_LOCATION,
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        # ... your default config...
        'allowedContent': True
    }
}

# Message storage
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ADMINS = [
    ('Admin name', 'admin.developer@gmail.com'),
]

# if managers != admins, do as ADMINS table (line 179-181) for managers
MANAGERS = ADMINS

# Extra deployment parameters
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 1800  # 30 minutes

# Email settings allowing you to send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

# your app email in google here
EMAIL_HOST_USER = 'example@gmail.com'

# your app email password in google here
EMAIL_HOST_PASSWORD = 'mypassword'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_LOCALTIME = True

# Language translation settings for french and haitian creole
# deactivate for now until translation feature is added

EXTRA_LANG_INFO = {
    'cr-ht': {
        'bidi': False,  # right-to-left
        'code': 'cr-ht',
        'name': 'Haitian Creole',
        'name_local': "Kreyòl",
    },
}

LANG_INFO = dict(locale.LANG_INFO, **EXTRA_LANG_INFO)
locale.LANG_INFO = LANG_INFO

LANGUAGES = (
    ('cr-ht', _('Kreyòl')),
    ('fr', _('Français')),
    ('en', _('English')),
)

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["cr-ht"]

LOCALE_PATHS = (
    os.path.join(BASE_DIR / 'locale'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}
