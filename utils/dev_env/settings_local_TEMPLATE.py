DATABASES = {
    'default' : {
        'ENGINE' : 'django.contrib.gis.db.backends.postgis',
        'NAME' : 'vegphilly',
        'USER' : 'vagrant',
        'PASSWORD' : '',
        'HOST' : '',
        'PORT' : '',
        }
}

try:
    from settings import INSTALLED_APPS
    INSTALLED_APPS += ('south', 'gunicorn', 'django.contrib.gis')
except ImportError:
    pass

