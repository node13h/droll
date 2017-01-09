"""
Django settings for droll project.

Generated by 'django-admin startproject' using Django 1.8.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


import os
import sys
import random
import string

import dj_database_url

from . import utils

env = utils.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get('SECRET_KEY') or ''.join(random.choice(
    ''.join([string.ascii_letters,
             string.digits,
             string.punctuation])) for _ in range(50))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get_bool('DEBUG')

TESTING = 'test' in sys.argv

PRODUCTION = not DEBUG and not TESTING

if PRODUCTION:
    MAILTO = env.get('MAILTO')
    if MAILTO:
        ADMINS = (('Admin', MAILTO), )

DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL') or 'webmaster@localhost'

ALLOWED_HOSTS = env.get_list('ALLOWED_HOSTS', ['*'])


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'droll.core',
    'droll.access',
    'droll.blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

if DEBUG and not TESTING:
    INSTALLED_APPS += (
        'django_extensions',
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INTERNAL_IPS = '127.0.0.1'

TEST_RUNNER = 'droll.tests.runner.DrollDiscoverRunner'

ROOT_URLCONF = 'droll.application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'droll.core.context_processors.site_title',
                'droll.core.context_processors.links',
            ],
        },
    },
]

WSGI_APPLICATION = 'droll.application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

FALLBACK_DEFAULT_DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}


DATABASES = {
    'default': dj_database_url.config() or FALLBACK_DEFAULT_DATABASE
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = env.get('LANGUAGE_CODE') or 'en-us'

TIME_ZONE = env.get('TIME_ZONE') or 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = env.get('STATIC_URL', '/static/')

AUTH_USER_MODEL = 'access.User'

OTP_VERIFY_URL = '/access/otp/'
OTP_SESSION_FLAG_NAME = 'otp_verified'


# Empty title is allowed
SITE_TITLE = env.get('SITE_TITLE', 'Let\'s roll')

static_backend = env.get('STATIC_BACKEND', 'local')

if static_backend == 'local':

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATIC_ROOT = env.get('STATIC_ROOT')

elif static_backend == 'sftp':

    STATICFILES_STORAGE = 'droll.core.storage_backends.SFTPStaticFilesStorage'

    STATIC_STORAGE_SFTP = {
        'HOST': env.get('STATIC_SFTP_HOST'),
        'CONNECT_PARAMS': {},
        'ROOT': env.get('STATIC_SFTP_ROOT'),
        'BASE_URL': env.get('STATIC_SFTP_BASE_URL', '/static/'),
    }

    sftpstorage_username = env.get('STATIC_SFTP_USERNAME')
    sftpstorage_password = env.get('STATIC_SFTP_PASSWORD')
    STATIC_SFTP_PARAMS = {}
    if sftpstorage_username:
        STATIC_STORAGE_SFTP['CONNECT_PARAMS']['username'] = sftpstorage_username
    if sftpstorage_password:
        STATIC_STORAGE_SFTP['CONNECT_PARAMS']['password'] = sftpstorage_password