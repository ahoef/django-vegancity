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



from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

import itertools
import geocode
import shlex

##########################################
# STATIC DATA
##########################################

CUISINE_TAGS = (
    ('chinese', 'Chinese'),
    ('thai', 'Thai'),
    ('mexican', 'Mexican'),
    ('italian', 'Italian'),
    ('middle_eastern', 'Middle Eastern'),
    ('southern', 'Southern'),
    ('soul_food', 'Soul Food'),
    ('vietnamese', 'Vietnamese'),
    ('indian', 'Indian'),
    ('ethiopian', 'Ethiopian'),
    ('pizza', 'Pizza'),
    ('bar_food', 'Bar Food'),
    ('fast_food', 'Fast Food'),
    ('pan_asian', 'Pan-Asian'),
    ('sushi', 'Sushi'),
    ('japanese', 'Japanese'),
    ('asian_fusion', 'Asian Fusion'),
    ('barbecue', 'Barbecue'),
    ('bakery', 'Bakery'),
    ('diner', 'Diner'),
    ('dim_sum', 'Dim Sum'),
    ('gastropub', 'Gastropub'),
    ('moroccan', 'Moroccan'),
    ('pakistani', 'Pakistani'),
    ('salads', 'Salads'),
    ('tapas', 'Tapas'),
    ('greek', 'Greek'),
    ('korean', 'Korean'),
    ('turkish', 'Turkish'),
    ('american', 'American'),
    ('african', 'African'),
    ('caribbean', 'Caribbean'),
    ('cajun', 'Cajun'),
    ('burgers', 'Burgers'),
    )

FEATURE_TAGS = (
    ('halal', 'Halal'),
    ('kosher', 'Kosher'),
    ('gluten_free_options', 'Gluten Free Options'),
    ('all_gluten_free', '100% Gluten Free'),
    ('gluten_free_desserts', 'Gluten Free Desserts'),
    ('vegan_desserts', 'Vegan Desserts'),
    ('fake_meat', 'Fake Meat'),
    ('cheese_steaks', 'Vegan Cheese Steaks'),
    ('sandwiches', 'Sandwiches'),
    ('coffeehouse', 'Coffeehouse'),
    ('food_cart', 'Food Cart'),
    ('cash_only', 'Cash Only'),
    ('delivery','Offers Delivery'),
    ('beer', 'Beer'),
    ('wine', 'Wine'),
    ('full_bar', 'Full Bar'),
    ('cheap', 'Cheap'),
    ('expensive', 'Expensive'),
    ('open_late', 'Open after 10pm'),
    ('smoothies', 'Smoothies/Juice Bar'),
    ('great_tea', 'Great Tea Selection'),
    ('byob', 'BYOB'),
    )

VEG_LEVELS = (
    (1, "100% Vegan"),
    (2, "Vegetarian - Mostly Vegan"),
    (3, "Vegetarian - Hardly Vegan"),
    (4, "Not Vegetarian"),
    (5, "Beware!"),
    )
    
RATINGS = tuple((i, i) for i in range(1, 5))


##########################################
# HELPERS / MANAGERS
##########################################

class VendorManager(models.Manager):
    "Manager class for handling searches by vendor."

    def get_query_set(self):
        "Changing initial queryset to ignore approved."
        # TODO - explore bugs this could cause!
        normal_qs = super(VendorManager, self).get_query_set()
        new_qs = normal_qs.filter(approved=True)
        return new_qs

    def pending_approval(self):
        """returns all vendors that are not approved, which are
        otherwise impossible to get in a normal query (for now)."""
        normal_qs = super(VendorManager, self).get_query_set()
        pending = normal_qs.filter(approved=False)
        return pending
        

    def tags_search(self, query, initial_queryset=None):
        """Search vendors by tag.

        Takes a query, breaks it into tokens, searches for tags
        that contain the token.  If any of the tokens match any
        tags, return all the orgs with that tag."""
        tokens = shlex.split(query)
        q_builder = Q()
        for token in tokens:
            q_builder = q_builder | Q(name__icontains=token)
        cuisine_tag_matches = CuisineTag.objects.filter(q_builder)
        feature_tag_matches = FeatureTag.objects.filter(q_builder)
        vendors = set()
        for tag in itertools.chain(cuisine_tag_matches, feature_tag_matches):
            qs = tag.vendor_set.all()
            if initial_queryset:
                qs = qs.filter(id__in=initial_queryset)
            for vendor in qs:
                vendors.add(vendor)
        vendor_count = len(vendors)
        summary_string = ('Found %d results with tags matching "%s".' 
                          % (vendor_count, ", ".join(tokens)))
        return {
            'count' : vendor_count, 
            'summary_statement' : summary_string, 
            'vendors':vendors
            }

    def name_search(self, query, initial_queryset=None):
        """Search vendors by name.

        Takes a query, breaks it into tokens, searches for names
        that contain the token.  If any of the tokens match any
        names, return all the orgs with that name."""
        tokens = shlex.split(query)
        q_builder = Q()
        for token in tokens:
            q_builder |= Q(name__icontains=token)
        vendors = self.filter(q_builder)
        if initial_queryset:
            vendors = vendors.filter(id__in=initial_queryset)
        vendor_count = vendors.count()
        summary_string = ('Found %d results where name contains "%s".' 
                          % (vendor_count, " or ".join(tokens)))
        return {
            'count' : vendor_count,
            'summary_statement' : summary_string, 
            'vendors' : vendors
            }

    #TODO - replace with something better!
    def address_search(self, query, initial_queryset=None):
        """ Search vendors by address.

        THIS WILL BE CHANGED SO NOT WRITING DOCUMENTATION."""
        
        if initial_queryset:
            vendors = self.filter(id__in=initial_queryset)

        # todo this is a mess!
        geocode_result = geocode.geocode_address(query)
        latitude, longitude, neighborhood = geocode_result
        point_a = (latitude, longitude)

        # TODO test this with a reasonable number of latitudes and longitudes
        lat_flr, lat_ceil, lng_flr, lng_ceil = geocode.bounding_box_offsets(point_a, 0.75)

        vendors_in_box = vendors.filter(latitude__gte=lat_flr,
                                     latitude__lte=lat_ceil,
                                     longitude__gte=lng_flr,
                                     longitude__lte=lng_ceil,)


        vendor_distances = geocode.distances(point_a, 
                                             [(vendor.latitude, vendor.longitude)
                                              for vendor in vendors_in_box])


        print vendors_in_box, vendor_distances
        vendor_pairs = zip(vendors_in_box, vendor_distances)

        sorted_vendor_pairs = sorted(vendor_pairs, key=lambda pair: pair[1][1])

        vendor_matches = filter(lambda pair: geocode.meters_to_miles(pair[1][1]) <= 0.75,
                                 sorted_vendor_pairs)

        vendors = map(lambda x: x[0], vendor_matches)
            
        vendor_count = len(vendors)
        summary_string = ('Found %d results where address is near "%s".' 
                          % (vendor_count, query))
        return {
            'count' : vendor_count, 
            'summary_statement' : summary_string, 
            'vendors':vendors
            }

##########################################
# SITE MODELS
##########################################

class Neighborhood(models.Model):
    """Used for tracking what neighborhood a vendor is in."""
    name = models.CharField(max_length=255)


class QueryString(models.Model):
    """All raw queries that users search by.

    Store the query and how it was ranked.  This
    is for researching how well the ranking algorithm
    is doing in predicting search types."""
    value = models.CharField(max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    rank_results = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.value

class BlogEntry(models.Model):
    "Blog entries.  They get entered in the admin."
    title = models.CharField(max_length=255)
    entry_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    text = models.TextField()

    class Meta:
        ordering = ('-entry_date',)

    def __unicode__(self):
        return self.title

##########################################
# VENDOR-RELATED MODELS
##########################################

class CuisineTag(models.Model):

    """Tags that describe vendor features.
   
    Example tags could be traditional ethnic cuisines
    like "mexican" or "french".  They could also
    be less traditional ones like "pizza" or
    "comfort" or "junk"."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.description

class FeatureTag(models.Model):
    """Tags that describe vendor features.
   
    Example tags would be "open late" or
    "offers delivery"."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.description

class VeganDish(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey('Vendor')

    def __unicode__(self):
        return self.name

class Review(models.Model):
    "The main class for handling reviews.  More or less requires a vendor."
    
    # CORE FIELDS
    vendor = models.ForeignKey('Vendor')
    author = models.ForeignKey(User, blank=True, null=True)

    # ADMINISTRATIVE FIELDS
    entry_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # DESCRIPTIVE FIELDS
    best_vegan_dish = models.ForeignKey(VeganDish, blank=True, null=True)
    unlisted_vegan_dish = models.CharField(
        "Favorite Vegan Dish (if not listed)", 
        max_length=100,
        help_text="We'll work on getting it in the database so others know about it!",
        blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "%s -- %s" % (self.vendor.name, str(self.entry_date))

class Vendor(models.Model):
    "The main class for this application"

    # CORE FIELDS
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    #neighborhood = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.ForeignKey(Neighborhood)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)

    # ADMINISTRATIVE FIELDS
    entry_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    objects = VendorManager()

    # DESCRIPTIVE FIELDS
    notes = models.TextField(blank=True, null=True,)
    veg_level = models.IntegerField(
        "How vegan friendly is this place?  See documentation for guildelines.",
        choices=VEG_LEVELS, 
        blank=True, null=True,)
    food_rating = models.IntegerField(choices=RATINGS, 
                                      blank=True, null=True,)
    atmosphere_rating = models.IntegerField(choices=RATINGS, 
                                            blank=True, null=True,)
    cuisine_tags = models.ManyToManyField(CuisineTag, null=True, blank=True)
    feature_tags = models.ManyToManyField(FeatureTag, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Steps to take before/after saving to db.

        Before saving, see if the vendor has been geocoded.
        If not, geocode."""
        if self.address and not (self.latitude and self.longitude):
            geocode_result  = geocode.geocode_address(self.address)
            if geocode_result:
                self.latitude, self.longitude, self.neighborhood = geocode_result
                
        super(Vendor, self).save(*args, **kwargs)

    def best_vegan_dish(self):
        "Returns the best vegan dish for the vendor"
        dishes = VeganDish.objects.filter(vendor=self)
        print dishes
        if dishes:
            return max(dishes, key=lambda d: Review.objects.filter(best_vegan_dish=d).count())
        else:
            return None

    def __unicode__(self):
        return self.name
