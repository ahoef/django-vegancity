from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

import geocode
import shlex

TAG_LIST = (
    ('chinese', 'Chinese'),
    ('delivery','Offers Delivery'),
    ('open_late', 'Open after 10pm'),
    )

VEG_LEVELS = (
    (1, "100% Vegan"),
    (2, "Vegetarian - Mostly Vegan"),
    (3, "Vegetarian - Hardly Vegan"),
    (4, "Not Vegetarian"),
    (5, "Beware!"),
    )
    
RATINGS = tuple((i, i) for i in range(1, 5))

class QueryString(models.Model):
    value = models.CharField(max_length=255)
    entry_date = models.DateTimeField()

    def __unicode__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class VendorManager(models.Manager):
    "Manager class for handling searches by vendor."

    def tags_search(self, query):
        """Search vendors by tag.

Takes a query, breaks it into tokens, searches for tags
that contain the token.  If any of the tokens match any
tags, return all the orgs with that tag."""
        tokens = shlex.split(query)
        q_builder = Q()
        for token in tokens:
            q_builder = q_builder | Q(name__icontains=token)
        tag_matches = Tag.objects.filter(q_builder)
        vendors = set()
        for tag in tag_matches:
            for vendor in tag.vendor_set.all():
                vendors.add(vendor)
        vendor_count = len(vendors)
        summary_string = ('Found %d results with tags matching "%s".' 
                          % (vendor_count, ", ".join(tokens)))
        return {
            'count' : vendor_count, 
            'summary_statement' : summary_string, 
            'vendors':vendors
            }

    def name_search(self, query):
        """Search vendors by name.

Takes a query, breaks it into tokens, searches for names
that contain the token.  If any of the tokens match any
names, return all the orgs with that name."""
        tokens = shlex.split(query)
        q_builder = Q()
        for token in tokens:
            q_builder |= Q(name__icontains=token)
        vendors = self.filter(q_builder)
        vendor_count = vendors.count()
        summary_string = ('Found %d results where name contains "%s".' 
                          % (vendor_count, " or ".join(tokens)))
        return {
            'count' : vendor_count,
            'summary_statement' : summary_string, 
            'vendors' : vendors
            }

    #TODO - replace with something better!
    def address_search(self, query):
        """ Search vendors by address.

THIS WILL BE CHANGED SO NOT WRITING DOCUMENTATION."""
        tokens = shlex.split(query)
        q_builder = Q()
        for token in tokens:
            q_builder |= Q(address__icontains=token)
        vendors = self.filter(q_builder)
        vendor_count = vendors.count()
        summary_string = ('Found %d results where address contains "%s".' 
                          % (vendor_count, " or ".join(tokens)))
        return {
            'count' : vendor_count, 
            'summary_statement' : summary_string, 
            'vendors':vendors
            }
        

class Vendor(models.Model):
    "The main class for this application"
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    website = models.URLField()
    notes = models.TextField(blank=True, null=True,)
    veg_level = models.IntegerField(choices=VEG_LEVELS, 
                                    blank=True, null=True,)
    food_rating = models.IntegerField(choices=RATINGS, 
                                      blank=True, null=True, )
    atmosphere_rating = models.IntegerField(choices=RATINGS, 
                                            blank=True, null=True,)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    objects = VendorManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.address and not (self.latitude and self.longitude):
            geocode_result = geocode.geocode_address(self.address)
            if geocode_result:
                self.latitude, self.longitude = geocode_result
        super(Vendor, self).save(*args, **kwargs)


    
class Review(models.Model):
    entry_date = models.DateTimeField()
    vendor = models.ForeignKey('Vendor')
    entered_by = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "%s -- %s" % (self.vendor.name, str(self.entry_date))
