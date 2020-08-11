from . settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj',
        'USER': 'dj',
        'PASSWORD': os.environ['POLLS_DB_PASSWORD'],
        'HOST': '127.0.0.1',
    },
    'presta': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gellifique',
        'USER': 'gellifique',
        'PASSWORD': os.environ['POLLS_DB_PASSWORD'],
        'HOST': '127.0.0.1',
    }
}  

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#FORCE_SCRIPT_NAME = '/pypy'
#STATIC_URL = FORCE_SCRIPT_NAME + '/static/'

WHITENOISE_STATIC_PREFIX = '/static/'
FORCE_SCRIPT_NAME = '/pypy'
STATIC_URL = '%s%s' % (FORCE_SCRIPT_NAME, WHITENOISE_STATIC_PREFIX)

DEBUG = True
