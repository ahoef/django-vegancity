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
    try:
        f = open(sys.argv[1], 'r')
    except IOError as e:
        print 'FILE NOT FOUND.'
        sys.exit()
    
    raw_string = f.read()
    lexer = lex.lex() 
    lexer.input(raw_string)
    result = [ ] 
    while True:
        tok = lexer.token()
        if not tok: break
        result = result + [(tok.type, tok.value)]

    name_indices = [i for i, v in enumerate(result) if v[0] == 'NAME']
    ranges = [range(name_indices[i], name_indices[i+1]) for i in range(len(name_indices) - 1)] + [range(name_indices[-1], len(result))]
    tuples_lists = (map(lambda x: map(lambda y: result[y], x), ranges))
    hashes = map(dict, tuples_lists)
    pprint.pprint(hashes)
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
            # add a tag for that vendor
            pass
        vendor.save()


def main():
    hashes = process_data()
    write_hashes(hashes)
    
    
    
if __name__ == '__main__':
    main()
