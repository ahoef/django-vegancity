from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

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
