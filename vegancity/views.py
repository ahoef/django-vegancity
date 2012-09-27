from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models

def vendors(request):
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

