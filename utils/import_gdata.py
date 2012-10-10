#!/usr/bin/env python

import sys
import pprint
import os
import imp
import pickle

from django.core.management import setup_environ

settings = imp.load_source('vegancity.settings', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "settings.py"))

setup_environ(settings)

models = imp.load_source('vegancity.models', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "models.py"))

tokens = ('NAME', 'ADDRESS', 'PHONE', 'URL', 'ZAGAT', 'CATEGORY', 'TAGS', 'REVIEW')


def unpickle_hashes(filename):
    f = open(filename, 'r')
    return pickle.load(f)

def write_hashes(hashes):
    for hash in hashes:
        vendor = models.Vendor()

        name = hash.get('NAME')
        if name:
            vendor.name = name

        address = hash.get('ADDRESS')
        if address:
            vendor.address = address

        phone = hash.get('PHONE')
        if phone:
            vendor.phone = phone

        url = hash.get('URL')
        if url:
            vendor.website = url
        
        vendor.approved = True
        vendor.save()

def write_tags():
    for tag in models.CUISINE_TAGS:
        t = models.CuisineTag()
        t.name = tag[0]
        t.description = tag[1]
        t.save()

    for tag in models.FEATURE_TAGS:
        t = models.FeatureTag()
        t.name = tag[0]
        t.description = tag[1]
        t.save()


def assign_tags():
    bb = models.Vendor.objects.get(name__icontains="blackbird")
    pizza = models.CuisineTag.objects.get(name__icontains="pizza")
    bb.cuisine_tags.add(pizza)

def main():
    hashes = unpickle_hashes('data.pickle')
    write_hashes(hashes)
    write_tags()
    assign_tags()
    
    
if __name__ == '__main__':
    main()
