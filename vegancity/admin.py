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

class ReviewAdmin(admin.ModelAdmin):
        list_display = ('vendor', 'approved',)
        list_filter = ('approved', 'best_vegan_dish', 'unlisted_vegan_dish')

class VendorAdmin(admin.ModelAdmin):
        list_display = ('id','approved', 'name', 'created', 'neighborhood')
        list_filter = ('approved',)

#####################################
## ADMIN REGISTRATION
#####################################

admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.QueryString)
admin.site.register(models.BlogEntry)
admin.site.register(models.VeganDish)
admin.site.register(models.CuisineTag)
admin.site.register(models.FeatureTag)
admin.site.register(models.Neighborhood)
