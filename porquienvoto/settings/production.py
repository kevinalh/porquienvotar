from .base import *

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    '''Get the environment variable or return exception'''
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("MY_KEY")

WSGI_APPLICATION = '/var/www/kevinalh_pythonanywhere_com_wsgi.py'
DEBUG = False

ALLOWED_HOSTS = ['kevinalh.pythonanywhere.com']

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kevinalh$pqvoto',
        'USER': 'kevinalh',
        'PASSWORD': 'thenemesis12*',
        'HOST': 'kevinalh.mysql.pythonanywhere-services.com',
        'OPTIONS': {
          'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}
