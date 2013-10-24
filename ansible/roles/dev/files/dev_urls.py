from django.conf.urls import patterns, include, url

localpatterns = patterns(url(r'^', include('debug_toolbar_htmltidy.urls')))
