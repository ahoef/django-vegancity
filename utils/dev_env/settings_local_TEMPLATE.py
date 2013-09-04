DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vegphilly',
        'USER': 'vegphilly',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DEVELOPMENT_APPS = (
    'debug_toolbar',
    'debug_toolbar_htmltidy',
)

DEVELOPMENT_MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',
)

EMAIL_HOST_USER = 'foo'
EMAIL_HOST_PASSWORD = 'bar'
