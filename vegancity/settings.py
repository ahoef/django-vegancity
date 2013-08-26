# Copyright (C) 2012 Steve Lamb

# This file is part of Vegancity.

# Vegancity is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Vegancity is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Vegancity.  If not, see <http://www.gnu.org/licenses/>.

from django.core.exceptions import ImproperlyConfigured
import os

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = "vegancity.UserProfile"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vegphilly',
        'USER': 'postgres',
    }
}

TIME_ZONE = None

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static/"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'insecure'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'vegancity.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

UNMANAGED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'vegancity',
    'south',
    'gunicorn',
)

MANAGED_APPS = (
    'vegancity',
)

INSTALLED_APPS = UNMANAGED_APPS + MANAGED_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'general': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/vegphilly/django-general.log',
            'maxBytes': 500000,
            'backupCount': 2,
            'formatter': 'simple',
        },
        'request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/vegphilly/django-request.log',
            'maxBytes': 500000,
            'backupCount': 2,
            'formatter': 'simple',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/vegphilly/django-sql.log',
            'maxBytes': 500000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'vegancity-general': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/vegphilly/vegancity-general.log',
            'maxBytes': 500000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'vegancity-search': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/vegphilly/vegancity-search.log',
            'maxBytes': 500000,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['general'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['request'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'WARN',
            'propagate': False,
        },
        'vegancity': {
            'handlers': ['vegancity-general'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'vegancity-search': {
            'handlers': ['vegancity-search'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

TEST_RUNNER = 'vegancity.tests.VegancityTestRunner'

###################################
# CUSTOM
###################################

# LOCATION_BOUNDS is the bounding box within which all data should live.
# This is used for a few different geospatial queries. Specify the
# southwest corner followed by the northeast corner in the format
# "sw_lat,sw_lng|ne_lat,ne_lng"
LOCATION_BOUNDS = "39.9269547,-75.2519587|39.988524,-75.106326"

# A string used to narrow down google maps searches. Consult
# the google maps javascript api v3 for more details.
LOCATION_COMPONENTS = "country:US|locality:Philadelphia"

# Used to specify where the map will center.
DEFAULT_CENTER = (39.946385, -75.1785634)

# Replace these with a valid gmail account login that
# can be used to send administrative emails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

try:
    from settings_local import *  # NOQA
except ImportError:
    pass


if EMAIL_HOST_USER == '' or EMAIL_HOST_PASSWORD == '':
    error_message = ("No valid email login configured. Please specify "
                     "EMAIL_HOST_USER and EMAIL_HOST_PASSWORD "
                     "in your settings_local.py file.")
    raise ImproperlyConfigured(error_message)
