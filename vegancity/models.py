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

import managers
import validators


#####################################
## HELPER CLASSES
#####################################

class NamedModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class NamedCreatedModel(NamedModel):
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True

class _TagModel(models.Model):
    name = models.CharField(
        help_text="short name, all lowercase alphas, underscores for spaces",
        max_length=255, unique=True
        )
    description = models.CharField(
        help_text="Nicely formatted text.  About a sentence.",
        max_length=255
        )
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.description
    
    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ('name',)

#######################################
# SITE CLASSES
#######################################

class VegLevel(NamedModel):
    description = models.TextField()
    super_category = models.CharField(max_length=30,
        choices=(
            ('vegan','Vegan'),
            ('vegetarian','Vegetarian'),
            ('not_veg', 'Not Vegetarian'),
            ('beware','Beware!')))

    def __unicode__(self):
        return "(%s) %s" % (self.super_category, self.description)

class Neighborhood(NamedCreatedModel):
    """Used for tracking what neighborhood a vendor is in."""
    class Meta:
        verbose_name = "Neighborhood"
        verbose_name_plural = "Neighborhoods"
        get_latest_by = "created"
        ordering = ('name',)

class QueryString(models.Model):
    """All raw queries that users search by.

    Store the query and how it was ranked.  This
    is for researching how well the ranking algorithm
    is doing in predicting search types."""
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    ranking_summary = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('created',)
        get_latest_by = "created"

    def __unicode__(self):
        return self.body

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

    
class CuisineTag(_TagModel):
    
    class Meta(_TagModel.Meta):
        verbose_name = "Cuisine Tag"
        verbose_name_plural = "Cuisine Tags"

class FeatureTag(_TagModel):
    
    class Meta(_TagModel.Meta):
        verbose_name = "Feature Tag"
        verbose_name_plural = "Feature Tags"


class VeganDish(NamedCreatedModel):
    vendor = models.ForeignKey('Vendor')

    class Meta:
        get_latest_by = "created"
        ordering = ('name',)
        verbose_name = "Vegan Dish"
        verbose_name_plural = "Vegan Dishes"


class Review(models.Model):
    "The main class for handling reviews.  More or less requires a vendor."
    
    # CORE FIELDS
    vendor = models.ForeignKey('Vendor')
    author = models.ForeignKey(User)

    # ADMINISTRATIVE FIELDS
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    objects = models.Manager()
    approved_objects = managers.ApprovedReviewManager()

    # DESCRIPTIVE FIELDS
    title = models.CharField(max_length=255, null=True, blank=True)
    food_rating = models.IntegerField(
        "How would you rate the food, overall?",
        choices=tuple((i, i) for i in range(1, 5)), 
        blank=True, null=True,)
    atmosphere_rating = models.IntegerField(
        "How would you rate the atmosphere?",
        choices=tuple((i, i) for i in range(1, 5)), 
        blank=True, null=True,)
    best_vegan_dish = models.ForeignKey(VeganDish, blank=True, null=True)
    unlisted_vegan_dish = models.CharField(
        "Favorite Vegan Dish (if not listed)",
        max_length=100,
        help_text="We'll work on getting it in the database so others know about it!",
        blank=True, null=True)
    suggested_feature_tags = models.CharField(max_length=255, blank=True, null=True)
    suggested_cuisine_tags = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(
        "Review", 
        help_text="NOTE: All slanderous reviews will be scrutinized. No trolling!")

    def __unicode__(self):
        return "%s -- %s" % (self.vendor.name, str(self.created))

    def get_absolute_url(self):
        return "/vendors/%d/" % self.vendor.id

    class Meta:
        get_latest_by = "created"
        ordering = ('created',)
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

class Vendor(NamedCreatedModel):
    "The main class for this application"

    # CORE FIELDS
    address = models.TextField(null=True)
    neighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, editable=False)
    phone = models.CharField(max_length=50, blank=True, null=True,
                             validators = [validators.validate_phone_number])
    website = models.URLField(blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True, editable=False)
    longitude = models.FloatField(default=None, blank=True, null=True, editable=False)

    # ADMINISTRATIVE FIELDS
    modified = models.DateTimeField(auto_now=True, null=True)
    approved = models.BooleanField(default=False)
    objects = managers.VendorManager()
    approved_objects = managers.ApprovedVendorManager()

    # DESCRIPTIVE FIELDS
    notes = models.TextField(blank=True, null=True,)
    veg_level = models.ForeignKey(VegLevel,
        help_text="How vegan friendly is this place?  See documentation for guildelines.",
        blank=True, null=True,)
    cuisine_tags = models.ManyToManyField(CuisineTag, null=True, blank=True)
    feature_tags = models.ManyToManyField(FeatureTag, null=True, blank=True)


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
        """Steps to take before/after saving to db.

        Before saving, see if the vendor has been geocoded.
        If not, geocode."""
        if self.needs_geocoding():
            self.apply_geocoding()
        super(Vendor, self).save(*args, **kwargs)

    def best_vegan_dish(self):
        "Returns the best vegan dish for the vendor"
        dishes = VeganDish.objects.filter(vendor=self)
        if dishes:
            return max(dishes, key=lambda d: Review.objects.filter(best_vegan_dish=d).count())
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
        reviews = Review.objects.filter(vendor=self)
        atmosphere_ratings = [review.atmosphere_rating for review in reviews if review.atmosphere_rating]
        if atmosphere_ratings:
            return sum(atmosphere_ratings) / len(atmosphere_ratings)
        else:
            return None

    def get_absolute_url(self):
        return "/vendors/%d/" % self.id

    class Meta:
        get_latest_by = "created"
        ordering = ('created',)
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
