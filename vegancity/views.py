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

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth import authenticate, login

from vegancity import forms
from vegancity import models
from vegancity import search

from django.db.models import Max

def home(request):
    "The view for the homepage."

    vendors = models.Vendor.approved_objects.all()
    top_5 = vendors.annotate(score=Sum('review__food_rating')).exclude(score=None).order_by('-score')[:5]
    recently_active = vendors.annotate(score=Max('review__created')).exclude(score=None).order_by('-score')[:5]

    neighborhoods = models.Neighborhood.objects.all()
    cuisine_tags = models.CuisineTag.objects.with_vendors()
    feature_tags = models.FeatureTag.objects.with_vendors()

    ctx = {
        'top_5': top_5,
        'recently_active' : recently_active,
        'neighborhoods': neighborhoods,
        'cuisine_tags' : cuisine_tags,
        'feature_tags' : feature_tags,
        }

    return render_to_response("vegancity/home.html", ctx,
                              context_instance=RequestContext(request))

def account_page(request):
    "The view for user accounts / profile pages."

    return render_to_response("vegancity/account_page.html",
                              context_instance=RequestContext(request))


def vendors(request):
    """Display table level data about vendors.

    If this view has a get param called query, then we trigger
    the search runmode.  Otherwise, we just return all vendors
    in our database."""

    search_form = forms.SearchForm(request.GET)
    
    # print "search_form.vendor_count:", search_form.vendor_count

    return render_to_response('vegancity/vendors.html', {'search_form':search_form},
                              context_instance=RequestContext(request))


###########################
## data entry views
###########################

def _generic_form_processing_view(request, form_obj, redirect_url, 
                                  template_name, pre_save_functions=[],
                                  form_init={}, ctx={}, commit_flag=False):
    """Generic view for form processing.

    Takes a number of arguments pertaining to the form processing
    and data entry process. Returns an HttpResponse and a model
    object.

    Call this function using another form processing view and return
    the HttpResponse.

    request: The HttpRequest that was received by the calling view.

    form_obj: A callable that returns a form object when called with
    no arguments or with a dictionary of POST data.

    redirect_url: A url object pointing to the redirection page in the
    event that the form processing is successful (valid).

    template_name: a string with the name of a template to render the
    form to.

    OPTIONAL:
    
    pre_save_functions: A list of callables that will be called, in order,
    with the model object, before saving to the database. Defaults to the
    empty list.

    form_init: a dictionary of initial data to be sent to the form if
    validation fails. Defaults to an empty dict.

    ctx: a context dictionary to be rendered into the template. The main
    form object will be placed in this dict with the name 'form'.
    """

    if request.method == 'POST':
        form = form_obj(request.POST)
        obj = None
        
        if form.is_valid():
            obj = form.save(commit=commit_flag)
            
            for fn in pre_save_functions:
                fn(obj)

            # If the object being edited has an approved attribute(field),
            # set approved to true for staff users
            if request.user.is_staff and 'approved' in dir(obj):
                setattr(obj, 'approved', True)

            obj.save()
            return HttpResponseRedirect(redirect_url), obj
        
    else:
        form = form_obj(initial=form_init)
        obj = None

    ctx['form'] = form
    
    return render_to_response(template_name, ctx, 
                              context_instance=RequestContext(request)), obj


def register(request):
    "Register a new user and log them in."

    response, obj =  _generic_form_processing_view(
        request, forms.VegUserCreationForm, 
        reverse("register_thanks"), 
        "vegancity/register.html",
        commit_flag=True)

    # if the registration was successful, log the user in
    if obj:
        new_user = authenticate(
            username=request.POST.get("username"), 
            password=request.POST.get("password1"))
        login(request, new_user)

    return response


@login_required
def new_vendor(request):
    "Create a new vendor."

    response, obj =  _generic_form_processing_view(
        request, 
        forms.NewVendorForm, 
        reverse("vendor_thanks"), 
        "vegancity/new_vendor.html")

    return response


@login_required
def new_review(request, vendor_id):
    "Create a new vendor-specific review."

    # get vendor, place in ctx dict for the template
    vendor = models.Vendor.approved_objects.get(id=vendor_id)
    ctx = {'vendor': vendor}

    # Apply the vendor as an argument to the form constructor.
    # This is done so that the form can be instantiated with
    # a single argument like a normal form constructor.
    form = functools.partial(forms.NewReviewForm, vendor)

    # a function for setting the author based on session data
    def apply_author(request, obj):
        obj.author = request.user
        return None

    # Apply the request as an argument to apply_author.
    # As above, this is done so the function can be callable
    # as apply_author(obj)
    apply_author = functools.partial(apply_author, request)
        
    response, obj =  _generic_form_processing_view(
            request, 
            form, 
            reverse("review_thanks", args=[vendor.id]),
            "vegancity/new_review.html", 
            [apply_author],
            {'vendor':vendor}, 
            ctx)

    return response
