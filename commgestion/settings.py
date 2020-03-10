"""
Django settings for commgestion project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import logging
import sys

import commgestion.config

from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Heuristic to see if we are running the development server.
RUNNING_DEV_SERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
RUNNING_MANAGE_COMMAND = (len(sys.argv) > 0 and sys.argv[0] == 'manage.py')

# Parse deployment specific configuration
try:
    config_path = os.path.join("/", "etc", "commgestion", "config.toml")
    config = commgestion.config.parse_from_file(config_path)
except FileNotFoundError as e:
    log.warning("Unable to find prod config at /etc/commgestion/config.toml")
    if not (RUNNING_DEV_SERVER or RUNNING_MANAGE_COMMAND):
        log.error("A prod config is required when not running the dev server.")
        raise e

    log.warning("Attempting to use the development configuration.")
    dev_config_path = os.path.join(BASE_DIR, "config-dev.toml")
    config = commgestion.config.parse_from_file(dev_config_path)

DEBUG = config["debug"]
if not RUNNING_DEV_SERVER and DEBUG:
    log.critical(
        "Running a debug server in production is a security vulnerability!")

ALLOWED_HOSTS = config["allowed_hosts"]
DATABASES = config["db"]
SECRET_KEY = config["secret_key"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'commgestion.urls'
APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'commgestion.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'


# WARNING / NOTE / READ THIS FIRST
# --------------------------------
# I wasted one hour on this issue here. If the languages that are listed here contain a '-' in them, the locales
# that are generated in the locale/ directory configured for this project expects to have an '_' instead and will NOT
# work if there is a '-'.
#
# Generate locale definitions: python manage.py makemessages -l <locale_> / django-admin makemessages -l <locale_>
# Compile locale translations: python manage.py compilemessage -l <locale_> / django-admin compilemessage -l <locale_>
#
# Additionally you could also use `--all`. All translatable strings needs to be discovered with {% trans ... %}

LANGUAGES = (
    ('en-us', _('English')),
    ('es-mx', _('Spanish')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = "/var/www/commgestion/static"
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
