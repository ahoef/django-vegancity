#
# This script will import data in to the database.
# It is written in python instead of some .sql format.
# This was done to make it easier to nuke the database,
# or switch between different databases.
# (we intend to move from sqlite to postgresql)
#

from django.core.management import setup_environ

import settings

setup_environ(settings)

import vegancity.models as models

vendor = models.Vendor()
vendor.name = "Steve's Grub"
vendor.veg_level = 1
vendor.food_rating = 1
vendor.service_rating = 1
vendor.atmosphere_rating = 1
vendor.save()

vendor = models.Vendor()
vendor.name = "Jeff's Tacos"
vendor.veg_level = 4
vendor.food_rating = 4
vendor.service_rating = 4
vendor.atmosphere_rating = 1
vendor.save()

vendor = models.Vendor()
vendor.name = "Bill's Blended Shakes"
vendor.veg_level = 1
vendor.food_rating = 1
vendor.service_rating = 1
vendor.atmosphere_rating = 1
vendor.save()

print "print all vendors:\n"

for vendor in models.Vendor.objects.all():
    print vendor.name

