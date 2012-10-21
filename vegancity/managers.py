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

import django.db.models as django_models
import shlex

import models

class VendorManager(django_models.Manager):
    "Manager class for handling searches by vendor."


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

class ApprovedVendorManager(VendorManager):
    def get_query_set(self):
        "Changing initial queryset to ignore approved."
        # TODO - explore bugs this could cause!
        normal_qs = super(VendorManager, self).get_query_set()
        new_qs = normal_qs.filter(approved=True)
        return new_qs

