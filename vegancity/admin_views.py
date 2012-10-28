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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import forms
import models
import itertools
import tracking

@staff_member_required
def pending_approval_count(request):
    pending_approval_count = (models.Vendor.objects.pending_approval().count() +
                              models.Review.objects.pending_approval().count())
    return HttpResponse(str(pending_approval_count))

@staff_member_required
def pending_approval(request):
    pending_vendors = models.Vendor.objects.pending_approval()
    pending_reviews = models.Review.objects.pending_approval()
    ctx = {
        'pending_vendors' : pending_vendors,
        'pending_reviews' : pending_reviews,
        }
    return render_to_response("admin/pending_approval.html", ctx,
                              context_instance=RequestContext(request))

@staff_member_required
def search_log(request):
    ctx = {
        'search_log': tracking.get_log(),
        }
    return render_to_response("admin/search_log.html", ctx,
                              context_instance=RequestContext(request))


@staff_member_required
def geocode_all(request):
    "Scan all vendors to determine if geocoding is needed and apply where needed."
    for vendor in models.Vendor.approved_objects.all():
        if vendor.needs_geocoding():
            vendor.apply_geocoding()
            vendor.save()
    return HttpResponseRedirect("/admin/")
