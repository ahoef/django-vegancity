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
from django.db.models import Sum
from django.contrib.auth import authenticate, login

from vegancity import forms
from vegancity import models
from vegancity import search


def home(request):
    vendors = models.Vendor.approved_objects.all()
    top_5 = vendors.annotate(score=Sum('review__food_rating')).order_by('score')[:5]
    recent_activity = models.Review.approved_objects.order_by("created")[:5]
    neighborhoods = models.Neighborhood.objects.all()
    cuisine_tags = models.CuisineTag.objects.with_vendors()
    feature_tags = models.FeatureTag.objects.with_vendors()

    ctx = {
        'top_5': top_5,
        'recent_activity' : recent_activity,
        'neighborhoods': neighborhoods,
        'cuisine_tags' : cuisine_tags,
        'feature_tags' : feature_tags,
        }

    return render_to_response("vegancity/home.html", ctx,
                              context_instance=RequestContext(request))

def vendors(request):
    """Display table level data about vendors.

    If this view has a get param called query, then we trigger
    the search runmode.  Otherwise, we just return all vendors
    in our database."""

    filter_form = forms.FilterForm(request.GET)
    
    if filter_form.is_valid():
        vendors = filter_form.get_pre_filtered_vendors()
        query = filter_form.query

    if query:
        vendors = search.master_search(query, vendors)

    filter_form.filter_selections_by_vendors(vendors)

    ctx = {
        'vendors' : vendors,
        'filter_form' : filter_form,
        }

    return render_to_response('vegancity/vendors.html', ctx,
                              context_instance=RequestContext(request))


###########################
## data entry views
###########################

def _generic_data_entry_view(request, form_obj, redirect_url, 
                             template_name, before_save_fns=[],
                             form_init={}, ctx={}):

    if request.method == 'POST':
        form = form_obj(request.POST)
        obj = None
        
        if form.is_valid():
            obj = form.save(commit=False)
            
            for fn in before_save_fns:
                fn(obj)

            if request.user.is_staff:
                if 'approved' in dir(obj):
                    obj.approved = True

            obj.save()
            return HttpResponseRedirect(redirect_url), obj
        
    else:
        form = form_obj(initial=form_init)
        obj = None

    ctx['form'] = form
    return render_to_response(template_name, ctx, context_instance=RequestContext(request)), obj


def register(request):
    response, obj =  _generic_data_entry_view(request, forms.VegUserCreationForm, reverse("register_thanks"), "vegancity/register.html")
    if obj:
        new_user = authenticate(username=request.POST.get("username"), password=request.POST.get("password1"))
        login(request, new_user)
    return response
    

@login_required
def new_vendor(request):
    response, obj =  _generic_data_entry_view(request, forms.NewVendorForm, reverse("vendor_thanks"), "vegancity/new_vendor.html")
    return response

@login_required
def new_review(request, vendor_id):
     vendor = models.Vendor.approved_objects.get(id=vendor_id)
     closed_form = functools.partial(forms.NewReviewForm, vendor)
     ctx = {'vendor': vendor}

     def apply_author(request, obj):
         obj.author = request.user
     
     apply_author = functools.partial(apply_author, request)
     
     response, obj =  _generic_data_entry_view(
         request, closed_form, reverse("review_thanks", args=[vendor.id]),
         "vegancity/new_review.html", [apply_author], 
         {'vendor':vendor}, ctx)

     return response
