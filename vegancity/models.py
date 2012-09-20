from django.db import models

VEG_LEVELS = (
    ('1', "100% Vegan"),
    ('2', "Vegetarian - Mostly Vegan"),
    ('3', "Vegetarian - Hardly Vegan"),
    ('4', "Not Vegetarian"),
    ('5', "Beware!"),
    )
    
RATINGS = tuple((i, i) for i in range(1, 5))

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    veg_level = models.IntegerField(choices=VEG_LEVELS)
    food_rating = models.IntegerField(choices=RATINGS)
    service_rating = models.IntegerField(choices=RATINGS)
    atmosphere_rating = models.IntegerField(choices=RATINGS)
    delivers = models.BooleanField(default=False)
    notes = models.TextField()

    def __unicode__(self):
        return self.name


