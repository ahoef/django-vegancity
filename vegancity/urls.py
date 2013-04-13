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

from vegancity import models, views

admin.autodiscover()


# CUSTOM VIEWS
urlpatterns = patterns('vegancity.views',
    url(r'^$', 'home', name='home'),
    url(r'^vendors/$', 'vendors', name="vendors"),
    url(r'^vendors/add/$', 'new_vendor', name="new_vendor"),
    url(r'^vendors/review/(?P<vendor_id>\d+)/$', 'new_review', name="new_review"),
    )

# GENERIC VIEWS
urlpatterns += patterns('',
    
    url(r'^blog/$', views.BlogView.as_view(), name="blog"),

    url(r'^vendors/(?P<pk>\d+)(-[\w\d]+)*/$',
        views.VendorDetailView.as_view(),
        name="vendor_detail"),

    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^privacy/$', views.PrivacyView.as_view(), name='privacy'),

    url(r'^vendors/review/(?P<pk>\d+)/thanks/$',
        views.ReviewThanksView.as_view(),
        name="review_thanks"),

    url(r'^vendors/add/thanks/$',
        views.VendorThanksView.as_view(),
        name="vendor_thanks"),
    url(r'^accounts/register/thanks/$',
        views.RegisterThanksView.as_view(),
        name='register_thanks'),
    )                        

# AUTH VIEWS
urlpatterns += patterns('',
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/'},  name='logout'),
    url(r'^accounts/register/$', 'vegancity.views.register', name='register'),
    url(r'^accounts/account_page/$', 'vegancity.views.account_page', name='account_page'),
    url(r'^accounts/account_page/edit/$', 'vegancity.views.account_edit', name='account_edit'),
)

# ADMIN VIEWS
if 'django.contrib.admin' in INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/pending_approval/$', 'vegancity.admin_views.pending_approval', name="pending_approval"),
        url(r'^admin/pending_approval/count/$', 'vegancity.admin_views.pending_approval_count', name="pending_approval_count"),
        # TODO this is a hack.
        # after overriding this url with a 410, i'm getting 'view does not exist' messages.
        # can't tell why.  For now, we'll just direct this url to a dummy view to avoid crashes.
        # Note that in the default setting for the site, review-add is disabled for all users.
        # however, if we ship this app, we can't take that for granted.
        url(r'^admin/vegancity/review/add/$', 'vegancity.admin_views.pending_approval'),
        url(r'^admin/', include(admin.site.urls)),
    )

