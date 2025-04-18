"""
Django settings for tucanapp project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import pymysql
pymysql.install_as_MySQLdb()
# import os
# import logging
# from logging.handlers import RotatingFileHandler

from pathlib import Path

import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kg!ll8fje%v92_g&o=wg3souibyzo1k*5$2y*4^au7ezzu*&@8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'users',
    'app',
    'deporte',
    'equipo',
    'jugador',
    'posicion',
    'configuracion_deporte',
    'logger',
    'evento',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Asegura que las respuestas sean JSON
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',  # Manejador de excepciones predeterminado
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tucanapp.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'tucanapp.wsgi.application'

# LOG_DIR = os.path.join(BASE_DIR, 'logs')
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'detailed': {
#             'format': '[{asctime}] [{levelname}] {name}: {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'WARNING',  # Captura advertencias, errores y críticas
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(LOG_DIR, 'django.log'),
#             'maxBytes': 5 * 1024 * 1024,  # 5 MB por archivo
#             'backupCount': 5,  # Mantiene hasta 5 archivos de backup
#             'formatter': 'detailed',
#         },
#         'http': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(LOG_DIR, 'http_requests.log'),
#             'maxBytes': 5 * 1024 * 1024,  
#             'backupCount': 3,
#             'formatter': 'detailed',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'detailed',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', 'console'],
#             'level': 'WARNING',
#             'propagate': True,
#         },
#         'django.request': {  # Captura errores HTTP como 404 y 500
#             'handlers': ['http', 'console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
CORS_ALLOW_ALL_ORIGINS = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tucanes',
        'USER': 'root', 
        'PASSWORD': 'root',
        'PORT': '3306',
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'users.CustomUser'

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#Configuración para Gmail
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Usar su correo de UTEZ
EMAIL_HOST_USER = "20213tn094@utez.edu.mx"
# Obtener de https://myaccount.google.com/apppasswords
EMAIL_HOST_PASSWORD = "xezs bppr ghox otpv"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')