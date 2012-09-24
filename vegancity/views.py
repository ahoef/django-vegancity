from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import models

def home(request):
    return render_to_response('vegancity/home.html', context_instance=RequestContext(request))

def spread(request):
    return render_to_response('vegancity/spread.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('vegancity/about.html', context_instance=RequestContext(request))

def search(request):
    vendors = models.Vendor.objects.all()
    ctx = {
        'vendors' : vendors,
        }
    return render_to_response('vegancity/search.html', ctx, context_instance=RequestContext(request))

