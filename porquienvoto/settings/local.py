from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pu2#sopq^_i@wmz91zg8+^+g-fec+ii9zl_99j4_w(y$*baszx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ("debug_toolbar", )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pqvoto',
        'USER': 'kevinalh',
        'PASSWORD': 'hermanos2',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#    'default': {
#         'ENGINE': 'mysql.connector.django',
#         'NAME': 'pqvoto',
#         'USER': 'kevinalh',
#         'PASSWORD': 'hermanos2',
#         'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }
