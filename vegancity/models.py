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
from django.db.models import Count

from django.template.defaultfilters import slugify

import shlex
import itertools
import geocode
import validators


class TagManager(models.Manager):
    """Manager class that can be used for any type of Tag class

    in this case, CuisineTag and FeatureTag"""
    def word_search(self, word):
        "takes a word and searches all tag names for that word"
        print "word:", word, "\n"
        qs = self.filter(name__icontains=word)
        if not qs and word[-1] == 's':
            qs = self.filter(name__icontains=word[:-1])
        return qs

    def with_vendors(self, vendors=None):
        "filters tags to tags that actually have vendors"
        qs = self.all()
        if vendors:
            qs = qs.filter(vendor__in=vendors).distinct('name')
        else:
            annotated = self.annotate(num_vendors=Count('vendor'))
            qs = annotated.filter(num_vendors__gte=1)
        return qs

    def get_vendors(self, qs):
        results = set()
        for tag in qs:
            results = results.union(tag.vendor_set.all())
        return results
        
class _TagModel(models.Model):
    """Abstract class that can be used for any type of Tag class

    in this case, CuisineTag and FeatureTag"""
    name = models.CharField(
        help_text="short name, all lowercase alphas, underscores for spaces",
        max_length=255, unique=True
        )
    description = models.CharField(
        help_text="Nicely formatted text.  About a sentence.",
        max_length=255
        )
    created = models.DateTimeField(auto_now_add=True, null=True)
    objects = TagManager()

    def __unicode__(self):
        return self.description

    def get_vendors(self):
        "returns all the vendors that are tagged with this tag."
        return self.vendor_set.all()
   
    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ('name',)

#######################################
# SITE CLASSES
#######################################

class VegLevel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    super_category = models.CharField(max_length=30,
        choices=(
            ('vegan','Vegan'),
            ('vegetarian','Vegetarian'),
            ('not_veg', 'Not Vegetarian'),
            ('beware','Beware!')))

    def __unicode__(self):
        return "(%s) %s" % (self.super_category, self.description)

class Neighborhood(models.Model):
    """Used for determining what neighborhood a vendor is in."""
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Neighborhood"
        verbose_name_plural = "Neighborhoods"
        get_latest_by = "created"
        ordering = ('name',)


##########################################
# USER-RELATED MODELS
##########################################

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    mailing_list = models.BooleanField(default=False)
    karma_points = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

class BlogEntry(models.Model):
    "Blog entries. They get entered in the admin."
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    body = models.TextField()

    class Meta:
        ordering = ('-created',)
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        get_latest_by = "created"

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return (reverse('blog_detail'), (str(self.id),))


##########################################
# VENDOR-RELATED MODELS
##########################################


class VeganDish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    vendor = models.ForeignKey('Vendor')

    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = "created"
        ordering = ('name',)
        verbose_name = "Vegan Dish"
        verbose_name_plural = "Vegan Dishes"

class ReviewManager(models.Manager):
    "Manager class for handling searches by review."


    def pending_approval(self):
        """returns all reviews that are not approved, which are
        otherwise impossible to get in a normal query (for now)."""
        normal_qs = self.get_query_set()
        pending = normal_qs.filter(approved=False)
        return pending


class ApprovedReviewManager(ReviewManager):
    "Manager for approved reviews only."

    def get_query_set(self):
        "Changing initial queryset to ignore approved."
        normal_qs = super(ApprovedReviewManager, self).get_query_set()
        new_qs = normal_qs.filter(approved=True)
        return new_qs


class Review(models.Model):
    "The main class for handling reviews.  More or less requires a vendor."
    
    # CORE FIELDS
    vendor = models.ForeignKey('Vendor')
    author = models.ForeignKey(User)

    # ADMINISTRATIVE FIELDS
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    objects = ReviewManager()
    approved_objects = ApprovedReviewManager()

    # DESCRIPTIVE FIELDS
    title = models.CharField(
        "Title of review (optional)",
        max_length=255, null=True, blank=True)
    food_rating = models.IntegerField(
        "How would you rate the food, overall?",
        choices=tuple((i, i) for i in range(1, 5)), 
        blank=True, null=True,)
    atmosphere_rating = models.IntegerField(
        "How would you rate the atmosphere?",
        choices=tuple((i, i) for i in range(1, 5)), 
        blank=True, null=True,)
    best_vegan_dish = models.ForeignKey(
        'VeganDish', 
        verbose_name="Favorite Vegan Dish",
        blank=True, null=True)
    unlisted_vegan_dish = models.CharField(
        "Favorite Vegan Dish (if not listed)",
        max_length=100,
        help_text="We'll post this on the site so others know about it.",
        blank=True, null=True)
    suggested_feature_tags = models.CharField(max_length=255, blank=True, null=True)
    suggested_cuisine_tags = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(
        "Review", 
        help_text="NOTE: All slanderous reviews will be scrutinized. No trolling!")

    def __unicode__(self):
        return "%s -- %s" % (self.vendor.name, str(self.created))

    def get_absolute_url(self):
        return "/vendors/%d-%s/" % (self.vendor.id, slugify(self.vendor.name))

    class Meta:
        get_latest_by = "created"
        ordering = ('created',)
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

class VendorManager(models.Manager):
    "Manager class for handling searches by vendor."

    def pending_approval(self):
        """returns all vendors that are not approved, which are
        otherwise impossible to get in a normal query (for now)."""
        normal_qs = super(VendorManager, self).get_query_set()
        pending = normal_qs.filter(approval_status='pending')
        return pending
        

    #TODO - replace with something better!
    def address_search(self, query):
        """ Search vendors by address.

        THIS WILL BE CHANGED SO NOT WRITING DOCUMENTATION."""
        
        vendors = self

        # todo this is a mess!
        geocode_result = geocode.geocode_address(query)

        if geocode_result == None:
            return []
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


        vendor_pairs = zip(vendors_in_box, vendor_distances)

        sorted_vendor_pairs = sorted(vendor_pairs, key=lambda pair: pair[1][1])

        vendor_matches = filter(lambda pair: geocode.meters_to_miles(pair[1][1]) <= 0.75,
                                 sorted_vendor_pairs)

        vendors = map(lambda x: x[0], vendor_matches)
            
        return vendors
    

class ApprovedVendorManager(VendorManager):
    """Manager for approved vendors only.

    Inherits the normal vendor manager."""
    def get_query_set(self):
        normal_qs = super(VendorManager, self).get_query_set()
        new_qs = normal_qs.filter(approval_status='approved')
        return new_qs


class Vendor(models.Model):
    "The main class for this application"

    # CORE FIELDS
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True)
    neighborhood = models.ForeignKey('Neighborhood', blank=True, null=True, editable=False)
    phone = models.CharField(max_length=50, blank=True, null=True,
                             validators = [validators.validate_phone_number])
    website = models.URLField(blank=True, null=True,
                             validators = [validators.validate_website])
    latitude = models.FloatField(default=None, blank=True, null=True, editable=False)
    longitude = models.FloatField(default=None, blank=True, null=True, editable=False)

    # ADMINISTRATIVE FIELDS
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    approval_status = models.CharField(max_length=100,
                                       choices = (('pending', 'Pending Approval'),
                                                  ('approved', 'Approved'),
                                                  ('quarantined', 'Quarantined')))
    objects = VendorManager()
    approved_objects = ApprovedVendorManager()

    # DESCRIPTIVE FIELDS
    notes = models.TextField(
        blank=True, null=True,
        help_text="Use this section to briefly describe the vendor. Notes will appear below the vendor's name.")
    veg_level = models.ForeignKey('VegLevel',
        help_text="How vegan friendly is this place?  See documentation for guildelines.",
        blank=True, null=True,)
    cuisine_tags = models.ManyToManyField('CuisineTag', null=True, blank=True)
    feature_tags = models.ManyToManyField('FeatureTag', null=True, blank=True)


    def needs_geocoding(self):
        """Returns true if the vendor is eligible for geocoding,
        but is missing geocoding data."""
        if self.latitude or self.longitude or self.neighborhood:
            return False

        elif not self.address:
            return False

        else:
            return True

    def apply_geocoding(self):

        geocode_result  = geocode.geocode_address(self.address)
        latitude, longitude, neighborhood = geocode_result

        if neighborhood:
            neighborhood_obj = None
            try:
                neighborhood_obj = Neighborhood.objects.get(name=neighborhood)
            except:
                pass

            if not neighborhood_obj:
                    neighborhood_obj = Neighborhood()
                    neighborhood_obj.name = neighborhood
                    neighborhood_obj.save()

            self.neighborhood = neighborhood_obj

        self.latitude = latitude
        self.longitude = longitude


    def save(self, *args, **kwargs):
        """Steps to take before saving to db.

        Before saving, see if the vendor has been geocoded.
        If not, geocode."""

        if self.pk is not None:
            orig_address = Vendor.objects.get(pk=self.pk).address
        else:
            orig_address = None
        if (orig_address != self.address) or self.needs_geocoding():
            self.apply_geocoding()
        super(Vendor, self).save(*args, **kwargs)

    def best_vegan_dish(self):
        "Returns the best vegan dish for the vendor"
        dishes = VeganDish.objects.filter(vendor=self)
        if dishes:
            return max(dishes, 
                       key=lambda d: Review.objects.filter(best_vegan_dish=d).count())
        else:
            return None

    def food_rating(self):
        reviews = Review.objects.filter(vendor=self)
        food_ratings = [review.food_rating for review in reviews if review.food_rating]
        if food_ratings:
            return sum(food_ratings) / len(food_ratings)
        else:
            return None

    def atmosphere_rating(self):
        "calculates the average rating for a vendor"
        reviews = Review.objects.filter(vendor=self)
        atmosphere_ratings = [review.atmosphere_rating for review in reviews 
                              if review.atmosphere_rating]
        if atmosphere_ratings:
            return sum(atmosphere_ratings) / len(atmosphere_ratings)
        else:
            return None

    def get_absolute_url(self):
        return "/vendors/%d-%s/" % (self.id, slugify(self.name))

    def __unicode__(self):
        return self.name

    def approved_reviews(self):
        return Review.approved_objects.filter(vendor=self.id)

    class Meta:
        get_latest_by = "created"
        ordering = ('name',)
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

#######################################
# TAGS
#######################################

class CuisineTag(_TagModel):

    class Meta(_TagModel.Meta):
        verbose_name = "Cuisine Tag"
        verbose_name_plural = "Cuisine Tags"

class FeatureTag(_TagModel):
    
    class Meta(_TagModel.Meta):
        verbose_name = "Feature Tag"
        verbose_name_plural = "Feature Tags"

