DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vegphilly',
        'USER': 'vagrant',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

EMAIL_HOST_USER = 'foo'
EMAIL_HOST_PASSWORD = 'bar'

try:
    from settings import INSTALLED_APPS
    INSTALLED_APPS += ('south', 'gunicorn')
except ImportError:
    pass
