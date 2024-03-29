from . settings import *

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj',
        'USER': 'gellifique',
        'PASSWORD': os.environ['POLLS_DB_PASSWORD'],
        #'HOST': '127.0.0.1',
        #'HOST': '172.31.17.32',
        'HOST': '172.31.14.216',
        #'HOST': '172.31.18.205',
    },
    'presta': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gellifique_new',
        'USER': 'gellifique',
        'PASSWORD': os.environ['POLLS_DB_PASSWORD'],
        #'HOST': '127.0.0.1',
        'HOST': '172.31.14.216',
        #'HOST': '172.31.18.205',
    },
}  

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WHITENOISE_STATIC_PREFIX = '/static/'
FORCE_SCRIPT_NAME = '/pyadmin734r04xdw'
STATIC_URL = '%s%s' % (FORCE_SCRIPT_NAME, WHITENOISE_STATIC_PREFIX)


DEBUG = True

sentry_sdk.init(
    environment="prod",
    dsn="https://2c7d92371b0143f982e0e528d8a519c8@o480612.ingest.sentry.io/5541486",
     integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
