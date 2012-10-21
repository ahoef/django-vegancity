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


def escape_single_quote(s):
    return s.replace("'", "''")

def main():
    hashes = unpickle_hashes('data.pickle')
    for hash in hashes:
        if hash.get("ADDRESS",""):
            print "('%s', '%s', '%s', '%s', t)," % (escape_single_quote(hash.get("NAME","")),
                                                escape_single_quote(hash.get("ADDRESS","")),
                                                escape_single_quote(hash.get("PHONE","")),
                                                escape_single_quote(hash.get("URL","")),)
    
if __name__ == '__main__':
    main()
