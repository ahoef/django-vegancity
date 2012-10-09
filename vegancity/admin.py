from django.contrib import admin
from models import Vendor, Review, QueryString, BlogEntry, VeganDish, CuisineTag, FeatureTag

# vendors
class VendorAdmin(admin.ModelAdmin):
    "Make it easier to admin the vendors"
    list_display = ('id','approved', 'name', 'entry_date')
    list_filter = ('approved',)

admin.site.register(Vendor, VendorAdmin)

# reviews
class ReviewAdmin(admin.ModelAdmin):
    "Make it easier to admin the reviews"
    list_display = ('id', 'approved', 'vendor',)
    list_filter = ('approved', 'best_vegan_dish', 'unlisted_vegan_dish')

admin.site.register(Review, ReviewAdmin)

# other
admin.site.register(QueryString)
admin.site.register(BlogEntry)
admin.site.register(VeganDish)
admin.site.register(CuisineTag)
admin.site.register(FeatureTag)


