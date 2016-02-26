"""
Django settings for porquienvoto project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz.apps.QuizConfig',
    'homepage.apps.HomepageConfig',
    'codificacion.apps.CodificacionConfig',
    'colorfield',
    'simple_history',
    'captcha',
    # 'django_pydenticon',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'porquienvoto.urls'

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
            # Cache loading
            # 'loaders': [
            #            ('django.template.loaders.cached.Loader', [
            #                'django.template.loaders.filesystem.Loader',
            #                'django.template.loaders.app_directories.Loader',
            #                ]
            #             ),
            # ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Autentificacion de usuarios

LOGIN_URL = 'login'

LOGOUT_URL = 'logout'

AUTH_PROFILE_MODULE = 'codificacion.PerfilUsuario'

LOGIN_REDIRECT_URL = 'cuenta/'

# Media

MEDIA_ROOT = 'codificacion/media'

MEDIA_URL = '/media/'

# Security - Scoop

DEBUG_PROPAGATE_EXCEPTIONS = False

# ReCaptcha

RECAPTCHA_PUBLIC_KEY = '6LcIVRkTAAAAAHNM1TEMwu1QNwJSZpIE4TOSWl3o'
RECAPTCHA_PRIVATE_KEY = '6LcIVRkTAAAAACW00u_PphLezFXHOYPia1VACoY0'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True
