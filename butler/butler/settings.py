"""
Django settings for butler project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import django.conf.global_settings as defaults


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    sys.stderr.write('No secret key set!\n')
    sys.exit(1)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

PROJECT_APPS = (
    'core',
    'systems',
    'dashboard'
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
    'djcelery',
    'gunicorn'

) + PROJECT_APPS


MIDDLEWARE_CLASSES = () + defaults.MIDDLEWARE_CLASSES

TEMPLATE_CONTEXT_PROCESSORS = (
    'dashboard.context_processors.add_dashboard_list',
) + defaults.TEMPLATE_CONTEXT_PROCESSORS

ROOT_URLCONF = 'butler.urls'

WSGI_APPLICATION = 'butler.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

import dj_database_url

if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'butler.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = False
USE_L10N = False
USE_TZ = True


# Graphite
GRAPHITE_SERVER = os.environ.get('GRAPHITE_SERVER', 'http://graphite.support.akvo-ops.org')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))


# Celery settings

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IMPORTS = (
    'systems.tasks',
)

BROKER_URL = os.environ.get('BROKER_URL', 'django://')
if BROKER_URL == 'django://':
    INSTALLED_APPS += ("kombu.transport.django",)

# Butler specific settings
PUPPETDB_URL = os.environ.get('PUPPETDB_URL')
PUPPETDB_KEY = os.environ.get('BUTLER_PUPPETDB_KEY')
PUPPETDB_CERT = os.environ.get('BUTLER_PUPPETDB_CERT')


# Cache configuration
CACHES = {
    'default': {
        'BACKEND': os.environ.get('CACHE_BACKEND', 'django.core.cache.backends.dummy.DummyCache'),
        'LOCATION': os.environ.get('CACHE_LOCATION', None),
        'TIMEOUT': 120
    },
}


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'butler': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# configure Celery from these settings
import djcelery
djcelery.setup_loader()
