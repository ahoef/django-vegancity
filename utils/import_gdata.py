#!/usr/bin/env python

# Copyright (C) 2012 Steve Lamb

# This file is part of Vegancity.

# Vegancity is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Vegancity is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Vegancity.  If not, see <http://www.gnu.org/licenses/>.


import sys
import pprint
import os
import imp
import pickle


from django.core.management import setup_environ

settings = imp.load_source('vegancity.settings', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "settings.py"))

setup_environ(settings)

models = imp.load_source('vegancity.models', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "models.py"))

from django.contrib.auth.models import User

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
    bb = models.Vendor.approved_objects.get(name__icontains="blackbird")
    pizza = models.CuisineTag.objects.get(name__exact="pizza")
    bb.cuisine_tags.add(pizza)

    vendor = models.Vendor.approved_objects.get(name__icontains="mi lah")
    cuisine = models.CuisineTag.objects.get(name__exact="chinese")
    vendor.cuisine_tags.add(cuisine)



    vendor = models.Vendor.approved_objects.get(name__icontains="Vedge")
    cuisine_tags = []
    for cuisine_tag in ['chinese','pan_asian', 'soul_food']:
        cuisine_tags.append(models.CuisineTag.objects.get(name__exact=cuisine_tag))
    vendor.cuisine_tags.add(*cuisine_tags)

    feature_tags = []
    for feature_tag in ['vegan_desserts', 'wine', 'beer', 'full_bar', 'expensive']:
        feature_tags.append(models.FeatureTag.objects.get(name__exact=feature_tag))
    vendor.feature_tags.add(*feature_tags)


    vendor = models.Vendor.approved_objects.get(name__icontains="maoz veg")
    cuisine_tags = []
    for cuisine_tag in ['middle_eastern', 'fast_food']:
        cuisine_tags.append(models.CuisineTag.objects.get(name__exact=cuisine_tag))
    vendor.cuisine_tags.add(*cuisine_tags)

    feature_tags = []
    for feature_tag in ['kosher', 'open_late', 'cheap']:
        feature_tags.append(models.FeatureTag.objects.get(name__exact=feature_tag))
    vendor.feature_tags.add(*feature_tags)

    vendor = models.Vendor.approved_objects.get(name__icontains="gourmet to go")
    cuisine_tags = []
    for cuisine_tag in ['fast_food']:
        cuisine_tags.append(models.CuisineTag.objects.get(name__exact=cuisine_tag))
    vendor.cuisine_tags.add(*cuisine_tags)

    feature_tags = []
    for feature_tag in ['kosher', 'open_late', 'cheap']:
        feature_tags.append(models.FeatureTag.objects.get(name__exact=feature_tag))
    vendor.feature_tags.add(*feature_tags)



def write_blog():
    blog = models.BlogEntry()
    blog.title = "Writing a test entry for the vegancity blog"
    blog.author = User.objects.get(id=1)
    blog.body = """Basically, you just have to create an import script and hack it out there.
                   You can try to get fancier than that, but I don't recommend it."""
    blog.save()


def main():
    hashes = unpickle_hashes('data.pickle')
    write_hashes(hashes)
    write_tags()
    assign_tags()
    write_blog()
    
    
if __name__ == '__main__':
    main()
