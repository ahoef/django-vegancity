#!/usr/bin/env python
# A module for taking a search query and deciding which resultset to show first.

# The idea is that queries with certain patterns are likely to be lumped as an
# address search, or a name search, etc.  This module contains tools for taking
# a query and returing a rank tuple of the form:
#
#     ((score, type_string), (score, type_string))
# ex. ((7, 'address'), (4, 'name'), (0, 'tag'))

import sys
import re


#######################
# STATIC CONTENT
#######################

# should we store this in the db?
_ADDRESS_PATTERNS = [
    (3, "\dth"), 
    (3, "\dst"), 
    (3, "\dnd"), 
    (3,  "\drd"), 
    (2, "near"),
    (2, " by "),
    (1, " and "), 
    (1, " & "),
    ]

# eventually we'll replace this with just the list of tags and a value of 5
_TAG_PATTERNS = [
    (5, "mexican"),
    (5, "italian"),
    (5, "chinese"),
    (5, "french"),
    (5, "comfort"),
    (5, "soul"),
    (5, "pizza"),
    ]

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
    return (_calculate_rank(query, _ADDRESS_PATTERNS), 'address')

def _tag_rank(query):
    return (_calculate_rank(query, _TAG_PATTERNS), 'tag')

def _name_rank(query):
    return (3, 'name')


#######################
# PUBLIC / RUNMODES
#######################

def get_ranks(query):
    "The primary external function.  Builds a rank summary."
    address = _address_rank(query)
    name = _name_rank(query)
    tag = _tag_rank(query)
    return sorted([address, name, tag], reverse=True)

def tests():
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
