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


from django.contrib import admin
import models
import forms

#####################################
## MODEL ADMIN CLASSES
#####################################

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('author','vendor',)
    list_display = ('vendor', 'author','approved',
                    'suggested_feature_tags', 'suggested_cuisine_tags',
                    
                    )
    list_filter = ('approved', 'unlisted_vegan_dish')
    form = forms.AdminEditReviewForm

class VeganDishInline(admin.TabularInline):
    model = models.VeganDish
    extra = 0

class VendorAdmin(admin.ModelAdmin):
    inlines = (VeganDishInline,)
    readonly_fields = ('latitude', 'longitude', 'neighborhood')
    list_display = ('approved', 'name', 'created', 'neighborhood')
    list_display_links = ('name',)
    list_editable = ('approved',)
    list_filter = ('approved',)
    filter_vertical = ('cuisine_tags','feature_tags',)


class BlogEntryAdmin(admin.ModelAdmin):

    exclude = ('author',)
    readonly_fields = ('author',)
    list_display = ('title','author','body')

    def save_model(self, request, blog_entry, form, change):
        blog_entry.author = request.user
        blog_entry.save()

    def queryset(self, request):
        qs = super(BlogEntryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

#####################################
## ADMIN REGISTRATION
#####################################

admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.QueryString)
admin.site.register(models.BlogEntry, BlogEntryAdmin)
admin.site.register(models.VeganDish)
admin.site.register(models.CuisineTag)
admin.site.register(models.FeatureTag)
admin.site.register(models.Neighborhood)
