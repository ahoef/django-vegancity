from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models

def vendors(request):

    if request.method == 'POST':
        raise AssertionError, "this shouldn't happen!"

    if request.GET:
        query = request.GET.get('query')
        vendors = models.Vendor.objects.filter(name__icontains=query)

        querystring = models.QueryString(value=query)
        querystring.save()

        result_set = [
            {
                'summary_statement' : "Found " + str(vendors.count()) + ' results where name contains "' + query + '".',
                'vendors' : vendors,
                }
            ]

    
    else:
        vendors = models.Vendor.objects.all()
        result_set = [
            {
                'summary_statement' : "We've got " + str(vendors.count()) + " food vendors in our database!",
                'vendors' : vendors,
                }
            ]

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
