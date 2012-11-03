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



# A module for taking a search query and deciding which resultset to show first.

# The idea is that queries with certain patterns are likely to be lumped as an
# address search, or a name search, etc.  This module contains tools for taking
# a query and returing a rank tuple of the form:
#
#     ((score, type_string), (score, type_string))
# ex. ((7, 'address'), (4, 'name'), (0, 'tags'))

import sys
import re
import shlex

# DIFFERENTIAL
# IF ONE SCORE IS HIGHER THAN ANOTHER SCORE BY THE DIFFERENTIAL
# THEN WE DON'T EVEN USE THAT TYPE OF SEARCH.
DIFF = 5

# THRESHOLD
# IF THE SCORE OF ANY SEARCH TYPE IS BELOW THE THRESHOLD,
# DON'T DO THAT SEARCH AT ALL
THRESHOLD = 5

FLUFF_WORDS = ("and", "or", "&", "the", "best")

def fluff_split(query):
    "takes a query and returns a list of non-fluff tokens"
    tokens = [token for token in query.split() if token not in FLUFF_WORDS]
    return tokens


#######################
# STATIC CONTENT
#######################

# should we store this in the db?
_ADDRESS_PATTERNS = (
    (3, "\dth"), 
    (3, "\dst"), 
    (3, "\dnd"), 
    (3,  "\drd"), 
    (2, "near"),
    (2, " by "),
    (1, " and "), 
    (1, " & "),
    )

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
    
# def _address_rank(query):
#     return (_calculate_rank(query, _ADDRESS_PATTERNS), 'address')

# def _tags_rank(query):
#     return (_calculate_rank(query, _TAGS_PATTERNS), 'tags')

# def _name_rank(query):
#     return (3, 'name')

def _address_rank(query):
    return _calculate_rank(query, _ADDRESS_PATTERNS)


#########################################
# PUBLIC / RUNMODES (CURRENTLY UNUSED)
#########################################

def get_ranks(query):
    "The primary external function.  Builds a rank summary."
    address = _address_rank(query)
    name = _name_rank(query)
    tags = _tags_rank(query)
    return sorted([address, name, tags], reverse=True)

def tests():
    # todo :  write tome tests
    pass

def main():
    tests()
    if len(sys.argv) > 1:
        results = ((query, get_ranks(query)) for query in sys.argv[1:])
        for result in results:
            query, ranks = result
            print query
            print result
            print

if __name__ == '__main__':
    main()


def master_search(query, initial_queryset=None):
    from vegancity.models import FeatureTag, CuisineTag, Vendor

    # take the query and do a featuretag and cuisine search on each word.
    real_words = fluff_split(query)

    name_words = set()
    name_vendors = set()
    name_rank = 0 # name gets no love initially

    tag_words = set()
    tag_vendors = set()
    tag_rank = 2 # tag is more likely, give it 2 for now

    for word in real_words:
        name_hits = Vendor.approved_objects.filter(name__icontains=word)
        print "name_hits:", name_hits, "\n"

        if name_hits:
            name_words.add(word)
            name_vendors = name_vendors.union(name_hits)
            name_rank += 1

        ft_hits = FeatureTag.objects.word_search(word)
        print "ft_hits:", ft_hits, "\n"
        ft_hits_vendors = FeatureTag.objects.get_vendors(ft_hits)
        print "ft_hits_vendors:", ft_hits_vendors, "\n"
        if ft_hits:
            tag_words.add(word)
            tag_vendors = tag_vendors.union(ft_hits_vendors)
            tag_rank += 1

        ct_hits = CuisineTag.objects.word_search(word)
        print "ct_hits:", ct_hits, "\n"
        ct_hits_vendors = CuisineTag.objects.get_vendors(ft_hits)
        print "ct_hits_vendors:", ct_hits_vendors, "\n"
        if ct_hits:
            tag_words.add(word)
            tag_vendors = tag_vendors.union(ct_hits_vendors)
            tag_rank += 1


    tag_word_density = float(len(tag_words)) / len(real_words)
    tag_rank += tag_word_density * 10

    name_word_density = float(len(name_words)) / len(real_words)
    name_rank += name_word_density * 10

    print "query:", query, "\n"
    tokens = shlex.split(query)
    print "tokens:", tokens, "\n"
    address_tokens = [token for token in tokens if token not in tag_words]
    print "address_tokens:", address_tokens, "\n"

    address_rank = 5 
    address_rank += _address_rank(query)
    # insert more statements that bump up the address rank.
    # might be nice to have a cache of street names.

    # THis will be the big block
    # where we go ahead and compare  
    # the namesearch, tagsearch, 
    # and address_presearch
    # STANDIN:
    rank_differential_test = (name_rank + tag_rank) / address_rank > 2
    print "rank_differential_test:", rank_differential_test
    
    master_results = []

    # always put name vendors at the top.
    # there won't be many!
    master_results.extend(name_vendors) 
    print "master_results:", master_results, "\n"
    
    lower_half_results = []
    if not rank_differential_test:
        address_search = Vendor.approved_objects.address_search(query)
        print "address_search:", address_search
        master_results.extend(address_search)

    print "master_results:", master_results, "\n"

    for name in tag_vendors:
        print "name:", name
        if name not in master_results:
            master_results.append(name)

    print "master_results:", master_results, "\n"
    return master_results


            

        
