from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models

def vendors(request):

    if request.method == 'POST':
        raise AssertionError, "this shouldn't happen!"

    if request.GET:
        vendors = models.Vendor.objects.filter(name__icontains=request.GET['query'])
    
    else:
        vendors = models.Vendor.objects.all()

    ctx = {
        'vendors' : vendors,
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
