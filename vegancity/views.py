from django.http import HttpResponse
from django.shortcuts import render_to_response, render


def home(request):
    return render_to_response('vegancity/home.html')
