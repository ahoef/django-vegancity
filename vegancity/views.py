from django.http import HttpResponse
from django.shortcuts import render_to_response, render

import models

def home(request):
    return render_to_response('vegancity/home.html')

def spread(request):
    return render_to_response('vegancity/spread.html')

def about(request):
    return render_to_response('vegancity/about.html')

def search(request):
    vendors = models.Vendor.objects.all()
    ctx = {
        'vendors' : vendors,
        }
    return render_to_response('vegancity/search.html', ctx)

