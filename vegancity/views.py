from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models

def search(request):
    vendors = models.Vendor.objects.all()
    ctx = {
        'vendors' : vendors,
        }
    return render_to_response('vegancity/search.html', ctx, context_instance=RequestContext(request))

