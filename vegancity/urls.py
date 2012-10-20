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


from django.conf.urls import patterns, include, url
from django.contrib import admin

from settings import INSTALLED_APPS

from vegancity.views import vendor_detail

admin.autodiscover()

# CUSTOM VIEWS
urlpatterns = patterns('vegancity.views',

    # vendors
    url(r'^vendors/$', 'vendors', name="vendors"),
    url(r'^vendors/add/$', 'new_vendor', name="new_vendor"),
    url(r'^vendors/(?P<vendor_id>\d+)/$', 'vendor_detail', name="vendor_detail"),

    # reviews
    url(r'^vendors/review/(?P<vendor_id>\d+)/$', 'new_review', name="new_review"),

    # blog
    url(r'^blog/$', 'blog', name="blog"),
    url(r'^blog/(?P<blog_entry_id>\d+)/$', 'blog_detail', name="blog_detail"),
    )

# GENERIC VIEWS
urlpatterns += patterns('django.views.generic.simple',
    
    # static pages
    url(r'^$', 'direct_to_template', {'template': 'vegancity/home.html'}, name='home'),
    url(r'^about/$', 'direct_to_template', {'template': 'vegancity/about.html'}, name='about'),
    )                        

# ADMIN VIEWS
if 'django.contrib.admin' in INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/pending_approval/', 'vegancity.admin_views.pending_approval', name="pending_approval"),
        url(r'^admin/', include(admin.site.urls)),
    )

# AUTH VIEWS
urlpatterns += patterns('',
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/'},  name='logout'),
    url(r'^accounts/register/$', 'vegancity.views.register', name='register'),
)
