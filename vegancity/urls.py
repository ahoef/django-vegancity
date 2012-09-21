from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'vegancity.views.home', name='home'),
    url(r'^search/$', 'vegancity.views.search', name='search'),
    url(r'^about/$', 'vegancity.views.about', name='about'),
    url(r'^spread/$', 'vegancity.views.spread', name='spread'),
    url(r'^create/$', 'vegancity.views.create', name='create'),
    url(r'^admin/', include(admin.site.urls)),
)
