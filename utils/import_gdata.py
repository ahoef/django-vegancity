#!/usr/bin/env python

import sys
import ply.lex as lex
import pprint
import os
import imp
import pickle

from django.core.management import setup_environ

settings = imp.load_source('vegancity.settings', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "settings.py"))

setup_environ(settings)

models = imp.load_source('vegancity.models', os.path.join(os.path.abspath(os.path.pardir),"vegancity", "models.py"))

tokens = ('NAME', 'ADDRESS', 'PHONE', 'URL', 'ZAGAT', 'CATEGORY', 'TAGS', 'REVIEW')

def remove_trailing(string):
    while string.endswith(" "):
        string = string[:-1]
    return string

def t_ADDRESS(token):
    r'[0-9A-Za-z #&]+,[ ][A-Za-z]+,[ ][A-Za-z]+'
    token.type = 'ADDRESS'
    return token

def t_PHONE(token):
    r'\([0-9]{3}\)[ ][0-9]{3}-[0-9]{4}'
    token.type = 'PHONE'
    return token

def t_URL(token):
    r'([-A-Za-z0-9]+\.)+(com|org|info|net)'
    token.type = 'URL'
    return token

def t_REVIEW_1(token):
    r'".*"[ ]-[^\n]*'
    token.type = 'REVIEW'
    return

def t_REVIEW_2(token):
    r'[^\n"]*"[^\n"]+"[^\n"]*'
    token.type = 'REVIEW'
    return

def t_REVIEW_3(token):
    r'[0-9 ]+review[^\n]*'
    token.type = 'REVIEW'
    return

def t_REVIEW_4(token):
    r'[^\n]*reviewer[^\n]*'
    token.type = 'REVIEW'
    return

def t_REVIEW_5(token):
    r'[^\n]*Diners\'[ ]Choice[^\n]*'
    token.type = 'REVIEW'
    return

def t_CATEGORY(token):
    r'Category:[^\n]+'
    token.type = 'CATEGORY'
    return token

def t_ZAGAT_STATS(token):
    r'[^\n]*(ZAGAT|reviews)[^\n]*'
    token.type = 'ZAGAT'
    return

def t_TAGS(token):
    r'([A-Za-z0-9\' ]+[ ]:::[ ])+[A-Za-z0-9\' ]+'
    token.type = 'TAGS'
    token.value = token.value.split(" ::: ")
    return token

def t_NAME(token):
    r'([^:]:[^:]|[-A-Za-z\' 0-9&,])+'
    token.type = 'NAME'
    token.value = remove_trailing(token.value)
    return token

t_ignore = ' \t\v\r'

def t_error(t):
  t.lexer.skip(1) 

def process_raw_data():
    "Takes raw data from .txt and lexes into python data structures"

    # read to file to string
    try:
        f = open(sys.argv[1], 'r')
    except IOError as e:
        print 'FILE NOT FOUND.'
        return None
    raw_string = f.read()


    # lex string into tokens collection
    lexer = lex.lex() 
    lexer.input(raw_string)

    # do i really have to use a while loop?
    # forloop failed, lexer.token() not iterable
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens += [(token.type, token.value)]

    # all_tags = set()
    # for tags in (token[1] for token in tokens if token[0] == 'TAGS'):
    #     for tag in tags:
    #         print tag
    #         all_tags.add(tag)

    # for tag in all_tags:
    #     print "    ('" + tag.replace(" ","_") + "','" + tag + "'),"

    # process tokens into hashes
    name_indices = [i for i, v in enumerate(tokens) if v[0] == 'NAME']
    ranges = [range(name_indices[i], name_indices[i+1]) for i in range(len(name_indices) - 1)] + [range(name_indices[-1], len(tokens))]
    tuples_lists = (map(lambda x: map(lambda y: tokens[y], x), ranges))
    hashes = map(dict, tuples_lists)
    return hashes

def pickle_hashes(hashes, filename):
    f = open(filename, 'w')
    pickle.dump(hashes, f)

def unpickle_hashes(filename):
    f = open(filename, 'r')
    return pickle.load(f)

def write_hashes(hashes):
    for hash in hashes:
        vendor = models.Vendor()

        name = hash.get('NAME')
        if name:
            vendor.name = name

        address = hash.get('ADDRESS')
        if address:
            vendor.address = address

        phone = hash.get('PHONE')
        if phone:
            vendor.phone = phone

        url = hash.get('URL')
        if url:
            vendor.website = url
        
        for tag in hash.get('TAGS',[]):
            pprint.pprint(tag)

        vendor.approved = True
        vendor.save()

def write_tags():
    for tag in models.CUISINE_TAGS:
        t = models.CuisineTag()
        t.name = tag[0]
        t.description = tag[1]
        t.save()

    for tag in models.FEATURE_TAGS:
        t = models.FeatureTag()
        t.name = tag[0]
        t.description = tag[1]
        t.save()


def assign_tags():
    bb = models.Vendor.objects.get(name__icontains="blackbird")
    pizza = models.CuisineTag.objects.get(name__icontains="pizza")
    bb.cuisine_tags.add(pizza)

def main():
    hashes = process_raw_data()
    write_hashes(hashes)
    write_tags()
    assign_tags()
    
    
if __name__ == '__main__':
    main()
