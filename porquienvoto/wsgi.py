# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/kevinalh/mysite/mysite/settings.py'
## and your manage.py is is at '/home/kevinalh/mysite/manage.py'
path = '/home/kevinalh/porquienvoto'
if path not in sys.path:
    sys.path.append(path)

os.environ['MY_KEY'] = 'pu2#sopq^_i@wmz91zg8+^+g-fec+ii9zl_99j4_w(y$*baszx'
os.environ['DJANGO_SETTINGS_MODULE'] = 'porquienvoto.settings.production'

## then, for django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

## or, for older django <=1.4
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
