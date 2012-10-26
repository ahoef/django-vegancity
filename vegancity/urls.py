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

from django.core.urlresolvers import reverse
from django.conf.urls import patterns, include, url
from django.contrib import admin

from settings import INSTALLED_APPS

import models
import api

admin.autodiscover()


# CUSTOM VIEWS
urlpatterns = patterns('vegancity.views',

    # vendors
    url(r'^vendors/$', 'vendors', name="vendors"),
    url(r'^vendors/add/$', 'new_vendor', name="new_vendor"),
 
    # reviews
    url(r'^vendors/review/(?P<vendor_id>\d+)/$', 'new_review', name="new_review"),
    )

# GENERIC VIEWS
urlpatterns += patterns('django.views.generic',
    
    url(r'^blog/$', 'list_detail.object_list', 
        {'queryset' : models.BlogEntry.objects.all(), 'template_name' : 'vegancity/blog.html' }, 
        name="blog"),

    # TODO: create template and uncomment
    # url(r'^blog/(?P<object_id>\d+)/$', 'list_detail.object_detail',
    #     {'queryset' : models.BlogEntry.objects.all(), 'template_name' : 'vegancity/blog_detail.html'}, 
    #     name="blog_detail"),

    url(r'^vendors/(?P<object_id>\d+)/$', 'list_detail.object_detail',
        {'queryset' : models.Vendor.approved_objects.all(), 'template_name' : 'vegancity/vendor_detail.html',
         'template_object_name' : 'vendor' }, name="vendor_detail"),

    # static pages
    url(r'^$', 'simple.direct_to_template', {'template': 'vegancity/home.html'}, name='home'),
    url(r'^about/$', 'simple.direct_to_template', {'template': 'vegancity/about.html'}, name='about'),
    )                        

# ADMIN VIEWS
if 'django.contrib.admin' in INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/pending_approval/$', 'vegancity.admin_views.pending_approval', name="pending_approval"),
        url(r'^admin/pending_approval/count/$', 'vegancity.admin_views.pending_approval_count', name="pending_approval_count"),
        url(r'^admin/geocode_all/', 'vegancity.admin_views.geocode_all', name="geocode_all"),
        # TODO this is a hack.
        # after overriding this url with a 410, i'm getting 'view does not exist' messages.
        # can't tell why.  For now, we'll just direct this url to a dummy view to avoid crashes.
        # Note that in the default setting for the site, review-add is disabled for all users.
        # however, if we ship this app, we can't take that for granted.
        url(r'^admin/vegancity/review/add/$', 'vegancity.admin_views.pending_approval'),
        url(r'^admin/', include(admin.site.urls)),
    )

# AUTH VIEWS
urlpatterns += patterns('',
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/'},  name='logout'),
    url(r'^accounts/register/$', 'vegancity.views.register', name='register'),
)


# vendor_resource = api.VendorResource()

# # API VIEWS
# urlpatterns += patterns('',
#     (r'^api/', include(vendor_resource.urls)),
#     )
