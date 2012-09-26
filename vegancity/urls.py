from django.conf.urls import patterns, include, url
from django.contrib import admin

from settings import INSTALLED_APPS

admin.autodiscover()

# CUSTOM VIEWS
urlpatterns = patterns('vegancity.views',
    url(r'^search/$', 'search', name='search'),
    )

# GENERIC VIEWS
urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'vegancity/home.html'}, name='home'),
    url(r'^about/$', 'direct_to_template', {'template': 'vegancity/about.html'}, name='about'),
    url(r'^spread/$','direct_to_template', {'template': 'vegancity/spread.html'}, name='spread'),
    )                        

# ADMIN VIEWS
if 'django.contrib.admin' in INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )
