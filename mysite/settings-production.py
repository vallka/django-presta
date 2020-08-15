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
    },
    'presta-testa': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gellifique_test',
        'USER': 'gel',
        'PASSWORD': os.environ['POLLS_DB_PASSWORD'],
        'HOST': '127.0.0.1',
    },
}  

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#FORCE_SCRIPT_NAME = '/pypy'
#STATIC_URL = FORCE_SCRIPT_NAME + '/static/'

WHITENOISE_STATIC_PREFIX = '/static/'
FORCE_SCRIPT_NAME = '/pypy'
STATIC_URL = '%s%s' % (FORCE_SCRIPT_NAME, WHITENOISE_STATIC_PREFIX)

DEBUG = True

sentry_sdk.init(
    environment="prod",
    dsn="https://21b5ea815b7a4191ade6d32c3dfac546@o360522.ingest.sentry.io/3651329",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
