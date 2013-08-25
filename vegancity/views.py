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
import logging

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count, Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import DetailView, TemplateView
from django.conf import settings

import django.contrib.auth.views

from vegancity import forms
from vegancity import models
from vegancity import search

search_logger = logging.getLogger('vegancity-search')

def password_change(request):
    response = django.contrib.auth.views.password_change(
        request, "registration/password_change_form.html",
        reverse('my_account'))

    # redirect happens when the form validates and the model saves
    if response.status_code == 302:
        messages.success(request, "Password Changed!")

    return response


def home(request):
    "The view for the homepage."

    vendors = models.Vendor.approved_objects.all()
    vendors_with_reviews = vendors.filter(review__approved=True).distinct()
    top_5 = vendors.annotate(fscore=Avg('review__food_rating'))\
                   .annotate(ascore=Avg('review__atmosphere_rating'))\
                   .exclude(fscore=None)\
                   .exclude(ascore=None)\
                   .order_by('-fscore', '-ascore')[:5]

    recently_active = vendors_with_reviews\
        .annotate(score=Max('review__created'))\
        .exclude(score=None)\
        .order_by('-score')[:5]

    recently_added = vendors.exclude(created=None).order_by('-created')[:5]

    most_reviewed = vendors_with_reviews.annotate(count=Count('review'))\
                                        .order_by('-count')[:5]

    neighborhoods = models.Neighborhood.objects.with_vendors()\
                                               .order_by('-vendor_count')[:21]

    cuisine_tags = models.CuisineTag.objects\
                                    .with_vendors()\
                                    .annotate(vcount=Count('vendor'))\
                                    .order_by('-vcount')[:21]

    feature_tags = models.FeatureTag.objects\
                                    .with_vendors()\
                                    .annotate(vcount=Count('vendor'))\
                                    .order_by('-vcount')[:21]

    ctx = {
        'top_5': top_5,
        'most_reviewed': most_reviewed,
        'recently_added': recently_added,
        'recently_active': recently_active,
        'neighborhoods': neighborhoods,
        'cuisine_tags': cuisine_tags,
        'feature_tags': feature_tags,
        }

    return render_to_response("vegancity/home.html", ctx,
                              context_instance=RequestContext(request))


def user_profile(request, username):
    if username is None:
        if request.user.username == '':
            raise Http404
        else:
            return redirect('user_profile', username=request.user.username)
    else:
        profile_user = get_object_or_404(models.User, username=username)
        reviews = models.Review.approved_objects.filter(author=profile_user)\
                                                .order_by('-created')
        return render_to_response(
            'vegancity/profile_page.html',
            {'profile_user': profile_user, 'reviews': reviews},
            context_instance=RequestContext(request))


def vendors(request):
    center_latitude, center_longitude = settings.DEFAULT_CENTER
    current_query = request.GET.get('current_query', None)
    previous_query = request.GET.get('previous_query', None)
    search_type = request.GET.get('search_type', None)
    selected_neighborhood = request.GET.get('neighborhood', None)
    selected_cuisine_tag_id = request.GET.get('cuisine_tag', None)
    selected_feature_tag_id = request.GET.get('feature_tag', None)
    checked_feature_filters = [f for f
                               in models.FeatureTag.objects.with_vendors()
                               if request.GET.get(f.name) or
                               selected_feature_tag_id == str(f.id)]

    vendors = models.Vendor.approved_objects.all()

    if selected_neighborhood:
        vendors = vendors.filter(neighborhood__id=selected_neighborhood)

    if selected_cuisine_tag_id:
        selected_cuisine_tag = models.CuisineTag.objects.get(
            pk=selected_cuisine_tag_id)
        vendors = vendors.filter(cuisine_tags__id=selected_cuisine_tag_id)
    else:
        selected_cuisine_tag = None

    if selected_feature_tag_id:
        vendors = vendors.filter(feature_tags__id=selected_feature_tag_id)

    for f in checked_feature_filters:
        vendors = vendors.filter(feature_tags__id__exact=f.id)

    vendors, search_type = search.filter_vendors_by_search(
        vendors, current_query, search_type)

    if current_query:
        current_query_blob = "%s searched for '%s', " % (request.user,
                                                         current_query)
        previous_query_blob = ("after searching for '%s', " % (previous_query)
                               if previous_query else "")
        results_blob = ("vendors returned were: %s" %
                        [v.id for v in vendors])
        log_message = current_query_blob + previous_query_blob + results_blob
        search_logger.info(log_message)

    ctx = {
        'cuisine_tags': models.CuisineTag.objects.all(),
        'feature_tags': models.FeatureTag.objects.all(),
        'neighborhoods': models.Neighborhood.objects.with_vendors(),
        'vendor_count': len(vendors),
        'vendors': vendors,
        'previous_query': previous_query,
        'current_query': current_query,
        'selected_cuisine_tag': selected_cuisine_tag,
        'checked_feature_filters': checked_feature_filters,
        'search_type': search_type,
        'has_get_params': len(request.GET) > 0,
        'center_latitude': center_latitude,
        'center_longitude': center_longitude,
    }
    return render_to_response('vegancity/vendors.html', ctx,
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

            if commit_flag is False:
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

    response, obj = _generic_form_processing_view(
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

    def apply_submitter(request, vendor):
        vendor.submitted_by = request.user

    apply_submitter = functools.partial(apply_submitter, request)

    response, obj = _generic_form_processing_view(
        request,
        forms.NewVendorForm,
        reverse("vendor_thanks"),
        "vegancity/new_vendor.html",
        [apply_submitter],
        commit_flag=False)

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

    response, obj = _generic_form_processing_view(
        request,
        form,
        reverse("review_thanks", args=[vendor.id]),
        "vegancity/new_review.html",
        [apply_author],
        {'vendor': vendor},
        ctx)

    return response


@login_required
def account_edit(request):
    """Edit page for user accounts"""

    user = request.user
    user_profile = user.get_profile()

    if request.method == 'POST':
        user_form = forms.VegUserEditForm(request.POST, instance=user)
        profile_form = forms.VegProfileEditForm(request.POST,
                                                instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile saved!')
        return HttpResponseRedirect(reverse('my_account'))
    else:
        user_form = forms.VegUserEditForm(instance=user)
        profile_form = forms.VegProfileEditForm(instance=user_profile)
    return render_to_response('vegancity/account_edit.html',
                              {'user_form': user_form,
                               'profile_form': profile_form},
                              context_instance=RequestContext(request))


###########################
## generic views
###########################

class VendorDetailView(DetailView):
    template_name = 'vegancity/vendor_detail.html'
    queryset = models.Vendor.approved_objects.all()


class AboutView(TemplateView):
    template_name = 'vegancity/about.html'


class PrivacyView(TemplateView):
    template_name = 'vegancity/privacy.html'


class ReviewThanksView(DetailView):
    template_name = 'vegancity/review_thanks.html'
    queryset = models.Vendor.approved_objects.all()

    def get_context_data(self, **kwargs):
        context = super(ReviewThanksView, self).get_context_data(**kwargs)
        context.update({'warning': True})
        return context


class VendorThanksView(TemplateView):
    template_name = 'vegancity/vendor_thanks.html'

    def get_context_data(self, **kwargs):
        context = super(VendorThanksView, self).get_context_data(**kwargs)
        context.update({'warning': True})
        return context


class RegisterThanksView(TemplateView):
    template_name = 'vegancity/register_thanks.html'
