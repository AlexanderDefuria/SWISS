"""
Django settings for FRC-Scouting project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
import boto3
from django.core.exceptions import ImproperlyConfigured

from django.forms.renderers import TemplatesSetting


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CSRF_TRUSTED_ORIGINS = ['https://*.swiss-scouting.ca']
CSRF_TRUSTED_ORIGINS = ['https://alexanderdefuria-urban-garbanzo-777gj97wxpjhrv59-8000.preview.app.github.dev']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'django_ajax',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'apps.entry.apps.EntryConfig',
    'apps.promotional.apps.PromotionalConfig',
    'apps.hours.apps.HoursConfig',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.entry.middleware.ValidateUser',
]

ROOT_URLCONF = 'FRC-Scouting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FRC-Scouting.wsgi.application'


# Forms
class CustomFormRenderer(TemplatesSetting):
    form_template_name = "entry/components/forms/experimental.html"

FORM_RENDERER = "FRC-Scouting.settings.CustomFormRenderer"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_secret("ENGINE"),
        'NAME': get_secret("NAME"),
        'USER': get_secret("USER"),
        'PASSWORD': get_secret("PASSWORD"),
        'HOST': get_secret("HOST"),
        'PORT': get_secret("PORT"),
        'OPTIONS': {'sslmode': get_secret("sslmode")},
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.entry.backends.HashedPasswordAuthBackend',
]

FIXTURE_DIRS = [
    'apps.entry.tests.test_data'
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# --------- Cookies ---------
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True

AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_S3_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
AWS_S3_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = get_secret("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = "nyc3"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_STATIC_LOCATION = get_secret("AWS_STATIC_LOCATION")
AWS_MEDIA_LOCATION = get_secret("AWS_MEDIA_LOCATION")

USE_STATIC_SPACES = get_secret("AWS_STATIC_LOCATION") != ""
USE_MEDIA_SPACES = get_secret("AWS_MEDIA_LOCATION") != ""

if USE_MEDIA_SPACES:
    # public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = '%s%s' % (AWS_S3_ENDPOINT_URL, AWS_MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = 'FRC-Scouting.storage_backends.MediaStorage'

else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    MEDIAFILES_DIRS = [
        os.path.join(BASE_DIR, "media")
    ]

if USE_STATIC_SPACES:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        os.path.join(BASE_DIR, "media/static"),
    ]
    STATIC_URL = '%s%s' % (AWS_S3_ENDPOINT_URL, AWS_STATIC_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    # STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        os.path.join(BASE_DIR, "media/static"),
    ]

print("MEDIA_URL:     " + MEDIA_URL)
print("STATIC_URL:    " + STATIC_URL)
print("DATABASE NAME: " + DATABASES.get('default').get('NAME'))