DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'vegphilly',
        'USER' : 'vagrant',
        'PASSWORD' : '',
        'HOST' : '',
        'PORT' : '',
        }
}

try:
    from settings import INSTALLED_APPS
    INSTALLED_APPS += ('south', 'gunicorn')
except ImportError:
    pass

