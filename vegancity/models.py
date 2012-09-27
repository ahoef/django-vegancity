from django.db import models
from django.contrib.auth.models import User

VEG_LEVELS = (
    (1, "100% Vegan"),
    (2, "Vegetarian - Mostly Vegan"),
    (3, "Vegetarian - Hardly Vegan"),
    (4, "Not Vegetarian"),
    (5, "Beware!"),
    )
    
RATINGS = tuple((i, i) for i in range(1, 5))

class Vendor(models.Model):
    "The main class for this application"
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    website = models.URLField()
    veg_level = models.IntegerField(choices=VEG_LEVELS, blank=True, null=True,)
    food_rating = models.IntegerField(choices=RATINGS, blank=True, null=True, )
    service_rating = models.IntegerField(choices=RATINGS, blank=True, null=True,)
    atmosphere_rating = models.IntegerField(choices=RATINGS, blank=True, null=True,)
    delivers = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True,)

    def __unicode__(self):
        return self.name


class Review(models.Model):
    entry_date = models.DateTimeField()
    vendor = models.ForeignKey('Vendor')
    entered_by = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return self.vendor.name + " --  " + str(self.entry_date)
