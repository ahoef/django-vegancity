#!/usr/bin/env python

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
"""
A module for taking a search query and deciding which resultset to
show first.

The idea is that queries with certain patterns are likely to be
lumped as an address search, or a name search, etc.  This module
contains tools for taking a query and returing a rank tuple of the
form:

((score, type_string), (score, type_string))

ex. ((7, 'address'), (4, 'name'), (0, 'tags'))
"""

import re
import geocode

from vegancity.models import FeatureTag, CuisineTag, Vendor

from django.contrib.gis.geos import Point


def fluff_split(query):
    "takes a query and returns a list of non-fluff tokens"
    FLUFF_WORDS = ("and", "or", "&", "the", "best")
    tokens = [token for token in query.split()
              if token not in FLUFF_WORDS and len(token) > 2]
    return tokens


#######################
# PRIVATE FUNCTIONS
#######################

def _calculate_rank(query, patterns):
    """Takes a query and patterns tuple and determines score."""
    rank = 0

    for pattern in patterns:
        score, regexp = pattern
        hits = re.findall(regexp, query)
        rank += score * len(hits)
    return rank


def _address_rank(query):
    ADDRESS_PATTERNS = (
        (3, "\dth"),
        (3, "\dst"),
        (3, "\dnd"),
        (3,  "\drd"),
        (2, "near"),
        (2, " by "),
        (1, " and "),
        (1, " & "),
        )
    return _calculate_rank(query, ADDRESS_PATTERNS)


#########################################
# PUBLIC / RUNMODES (CURRENTLY UNUSED)
#########################################

def name_search(query, initial_queryset=None):
    words = query.split()
    name_words = set()
    name_vendors = set()
    name_rank = 0  # name gets no love initially

    for word in words:
        name_hits = Vendor.approved_objects.filter(name__icontains=word)

        if name_hits:
            name_words.add(word)
            name_vendors = name_vendors.union(name_hits)
            name_rank += 1

    name_word_density = float(len(name_words)) / len(words)
    name_rank += name_word_density * 10

    if initial_queryset:
        name_vendors = [v for v in name_vendors if v in initial_queryset]

    return name_vendors, name_rank


def tag_search(query, initial_queryset=None):
    words = query.split()
    tag_words = set()
    tag_vendors = set()
    tag_rank = 2  # tag is more likely, give it 2 for now

    for word in words:
        ft_hits = FeatureTag.objects.word_search(word)
        ft_hits_vendors = FeatureTag.objects.get_vendors(ft_hits)
        if ft_hits:
            tag_words.add(word)
            tag_vendors = tag_vendors.union(ft_hits_vendors)
            tag_rank += 1

        ct_hits = CuisineTag.objects.word_search(word)
        ct_hits_vendors = CuisineTag.objects.get_vendors(ct_hits)
        if ct_hits:
            tag_words.add(word)
            tag_vendors = tag_vendors.union(ct_hits_vendors)
            tag_rank += 1

    tag_word_density = float(len(tag_words)) / len(words)
    tag_rank += tag_word_density * 10

    if initial_queryset:
        tag_vendors = [v for v in tag_vendors if v in initial_queryset]

    return tag_vendors, tag_rank


def address_search(query, initial_queryset=None):
    address_rank = 8
    address_rank += _address_rank(query)

    address_vendors = perform_address_search(Vendor.approved_objects.all(),
                                             query)

    if initial_queryset:
        address_vendors = [v for v in address_vendors
                           if v in initial_queryset]

    return address_vendors, address_rank


def master_search(query, initial_queryset=None):
    address_vendors, address_rank = address_search(query)
    name_vendors, name_rank = name_search(query)
    tag_vendors, tag_rank = tag_search(query)

    search_type = ""
    master_results = []
    best_score = max(address_rank, tag_rank, name_rank)
    if address_rank == best_score:
        search_type = "address"
        master_results = address_vendors
    elif name_rank == best_score:
        search_type = "name"
        master_results = name_vendors
    else:
        search_type = "tag"
        master_results = tag_vendors

    if initial_queryset:
        master_results = [vendor for vendor in master_results
                          if vendor in initial_queryset]
    return master_results, search_type


def perform_address_search(initial_queryset, query):
        vendors = initial_queryset

        # todo this is a mess!
        geocode_result = geocode.geocode_address(query)

        if geocode_result is None:
            return []
        latitude, longitude, neighborhood = geocode_result

        point = Point(x=longitude, y=latitude, srid=4326)
        vendors = Vendor.objects.filter(location__dwithin=(point, .004))

        return vendors
