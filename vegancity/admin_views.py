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

from django.contrib.admin.views.decorators import staff_member_required

import forms
import models
import itertools
import csv
import datetime

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

def csv_filename_builder(filename_prefix):
    """
    Takes a filename prefix and returns an HttpResponse with headers
    set for csv and with a filename that is uniquified using the
    current date.

    ex:
    'vegphilly_ml' -> response with 'vegphilly_ml_20130504.csv'
    """

    formatted_datestring = datetime.date.today().strftime("%Y%m%d")

    filename_param = "filename = %s_%s.csv" % (filename_prefix,
                                               formatted_datestring)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; %s;' % filename_param

    return response
    

@staff_member_required
def mailing_list(request):
    response = csv_filename_builder('vegphilly_ml')

    mailing_list_users = models.User.objects.filter(
        userprofile__mailing_list=True)

    writer = csv.writer(response)
    writer.writerow(['username', 'firstname', 'lastname', 'email'])

    for user in mailing_list_users:
        writer.writerow([user.username, user.first_name,
                         user.last_name, user.email])
    
    return response

@staff_member_required
def vendor_list(request):
    response = csv_filename_builder('vegphilly_vendors')

    vendors = models.Vendor.approved_objects.all()

    writer = csv.writer(response)
    writer.writerow(['name',
                     'address',
                     'neighborhood',
                     'phone',
                     'website',
                     'veg_level',
                     'notes'])

    for vendor in vendors:
        writer.writerow([vendor.name,
                         vendor.address,
                         vendor.neighborhood,
                         vendor.phone,
                         vendor.website,
                         vendor.veg_level,
                         vendor.notes])
    
    return response
