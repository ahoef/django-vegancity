from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models
import itertools

def vendors(request):

    if request.method == 'POST':
        raise AssertionError, "this shouldn't happen!"

    query = request.GET.get('query', '')
    
    vendors = models.Vendor.objects.all()

    if query:

        querystring = models.QueryString(value=query)
        querystring.save()

        name_vendors = vendors.filter(name__icontains=query)
        address_vendors = vendors.filter(address__icontains=query)

        vendors = [vendor for vendor in vendors if vendor in itertools.chain(name_vendors, address_vendors)]

        result_set = [
            {'summary_statement' : 'Found %d results where name contains "%s".'
             % (name_vendors.count(), query),
                'vendors' : name_vendors,},
            {'summary_statement' : 'Found %d results where address contains "%s".'
             % (address_vendors.count(), query),
                'vendors' : address_vendors,},
            ]

    
    else:
        result_set = [{'summary_statement' : "We've got %d food vendors in our database!" 
             % vendors.count(),
                'vendors' : vendors,}]

    ctx = {
        'vendors' : vendors,
        'result_set' : result_set,
        }
    return render_to_response('vegancity/vendors.html', ctx, context_instance=RequestContext(request))

def vendor_detail(request, vendor_id):
    vendor = models.Vendor.objects.get(id=vendor_id)
    reviews = models.Review.objects.filter(vendor__id=vendor_id)
    ctx = {
        'vendor' : vendor,
        'reviews' : reviews,
        }
    return render_to_response('vegancity/vendor_detail.html', ctx, context_instance=RequestContext(request))

def new_vendor(request):
    if request.method == 'GET':
        # the person is visiting the page for the first time
        pass

    elif request.method == 'POST':
        # the person just posted some data
        pass
