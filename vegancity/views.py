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

import functools
import itertools

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from vegancity import forms
from vegancity import models

def vendors(request):
    """Display table level data about vendors.

    If this view has a get param called query, then we trigger
    the search runmode.  Otherwise, we just return all vendors
    in our database."""

    # TODO: this view is a mess. Most of this stuff should be moved
    # to model managers.

    # figure out which filters have been checked
    all_feature_tags = models.FeatureTag.objects.with_vendors()
    checked_feature_filters = [f for f in all_feature_tags
                               if request.GET.get(f.name)]
    selected_cuisine = request.GET.get('cuisine', None)
    selected_neighborhood = request.GET.get('neighborhood', None)

    # Filter the set of vendors that can be displayed
    # based on what is in the checked filters.
    vendors = models.Vendor.approved_objects.all()

    for f in checked_feature_filters:
        vendors = vendors.filter(feature_tags__id__exact=f.id)

    if selected_neighborhood:
        vendors = vendors.filter(neighborhood__name=selected_neighborhood)

    if selected_cuisine:
        vendors = vendors.filter(cuisine_tags__name=selected_cuisine)

    # determine which filters can be presented on the page
    # based on whether they apply to any of the remaining
    # vendors
    available_feature_filters = [tag for tag in all_feature_tags if 
                       tag.vendor_set.filter(id__in=vendors)]

    query = request.GET.get('query', '')

    if query:
        vendors = models.Vendor.objects.search(query, vendors)

    ctx = {
        'vendors' : vendors,
        'query': query,

        'feature_filters' : available_feature_filters,
        'cuisines' : models.CuisineTag.objects.with_vendors(),
        'neighborhoods' : models.Neighborhood.objects.all(),

        'checked_feature_filters' : checked_feature_filters,
        'selected_neighborhood' : selected_neighborhood,
        'selected_cuisine' : selected_cuisine,
        }

    return render_to_response('vegancity/vendors.html', ctx,
                              context_instance=RequestContext(request))



###########################
## data entry views
###########################

def _generic_data_entry_view(request, closed_form, redirect_url, 
                       template_name, form_init={}, ctx={}, apply_author=False):

    if request.method == 'POST':
        form = closed_form(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            
            if apply_author:
                obj.author = request.user

            if request.user.is_staff:
                if 'approved' in dir(obj):
                    obj.approved = True
            obj.save()
            return HttpResponseRedirect(redirect_url)
        
    else:
        form = closed_form(initial=form_init)

    ctx['form'] = form
    return render_to_response(template_name, ctx,
                              context_instance=RequestContext(request))


def register(request):
    return _generic_data_entry_view(request, forms.VegUserCreationForm, reverse("home"), "vegancity/register.html")

@login_required
def new_vendor(request):
    return _generic_data_entry_view(request, forms.NewVendorForm, reverse("vendors"), "vegancity/new_vendor.html")

@login_required
def new_review(request, vendor_id):
     vendor = models.Vendor.approved_objects.get(id=vendor_id)
     closed_form = functools.partial(forms.NewReviewForm, vendor)
     ctx = {'vendor': vendor}
     
     return _generic_data_entry_view(
         request, closed_form, reverse("vendor_detail", args=[vendor.id]),
         "vegancity/new_review.html", {'vendor':vendor}, ctx, True)
