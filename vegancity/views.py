from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

import forms

import models
import itertools
import rank
import tracking

def vendors(request):
    """Display table level data about vendors.

If this view has a get param called query, then we trigger
the search runmode.  Otherwise, we just return all vendors
in our database.

Most of the complexity in this view is due to the ordering
of results.  This view tries to decide what type of search
the user is executing and display results accordingly."""

    query = request.GET.get('query', '')
    
    vendors = models.Vendor.objects.all()

    if query:

        # rank the likelihood of different search times
        ranks = rank.get_ranks(query)
        presentation_order = (rank[1] for rank in ranks)

        # log the query in the db
        tracking.log_query(query, ranks)

        # execute searches and store them in a hash
        searches = {
            'name' : models.Vendor.objects.name_search(query),
            'address' : models.Vendor.objects.address_search(query),
            'tags' : models.Vendor.objects.tags_search(query),
            }

        # compute the set of all vendors found in the 3 searches
        # todo - optimize?
        vendors = [vendor for vendor in vendors if vendor in 
                   itertools.chain(searches['name']['vendors'], 
                                   searches['address']['vendors'], 
                                   searches['tags']['vendors'])]

        result_set = map(lambda x: searches[x], presentation_order)
    
    else:
        # There was no search, show em all!
        result_set = [
            {'summary_statement' : 
             "We've got %d food vendors in our database!"
             % vendors.count(), 'vendors' : vendors,}]

    ctx = {
        'vendors' : vendors,
        'result_set' : result_set,
        }
    return render_to_response('vegancity/vendors.html', ctx,
                              context_instance=RequestContext(request))


def vendor_detail(request, vendor_id):
    """Display record level detail about a vendor.

Also grabs reviews and sends them to the template."""
    vendor = models.Vendor.objects.get(id=vendor_id)
    reviews = models.Review.objects.filter(vendor__id=vendor_id)
    ctx = {
        'vendor' : vendor,
        'reviews' : reviews,
        }
    return render_to_response('vegancity/vendor_detail.html', ctx, 
                              context_instance=RequestContext(request))


def blog(request):
    blog_entries = models.BlogEntry.objects.all()
    ctx = {
        'blog_entries' : blog_entries,
        }
    return render_to_response('vegancity/blog.html', ctx,
                              context_instance=RequestContext(request))

def blog_detail(request, blog_entry_id):
    blog_entry = models.BlogEntry.objects.get(id=blog_entry_id)
    ctx = {
        'blog_entry' : blog_entry,
        }
    return render_to_response('vegancity/blog_detail.html', ctx,
                              context_instance=RequestContext(request))
    

def register(request):
    if request.method == 'POST':
        form = forms.VegUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = forms.VegUserCreationForm()
    return render_to_response("vegancity/register.html", {'form': form},
                              context_instance=RequestContext(request))


###########################
## data entry views
###########################

@login_required
def new_vendor(request):
    if request.method == 'POST':
        form = forms.NewVendorForm(request.POST)
        if form.is_valid():
            new_vendor = form.save()
            return HttpResponseRedirect(reverse("vendors"))
    else:
        form = forms.NewVendorForm()
    return render_to_response("vegancity/new_vendor.html", {'form': form},
                              context_instance=RequestContext(request))

@login_required
def new_review(request, vendor_id):
    
    vendor = models.Vendor.objects.get(id=vendor_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(vendor, request.POST)
        if review_form.is_valid():
            review = models.Review()
            review.vendor = review_form.cleaned_data['vendor']
            review.entered_by = request.user
            review.content = review_form.cleaned_data['content']
            review.best_vegan_dish = review_form.cleaned_data['best_vegan_dish']
            review.save()
            return HttpResponseRedirect(reverse("vendors"))
    else:
        review_form = forms.ReviewForm(vendor_id,
            initial={'vendor': vendor})

    ctx = {
        'vendor' : vendor,
        'form' : review_form,
        }

    return render_to_response("vegancity/review.html", ctx,
                              context_instance=RequestContext(request))
