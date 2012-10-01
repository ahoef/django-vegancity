import re
import models

def calculate_rank(query, patterns):
    rank = 0

    for pattern in patterns:
        score, regexp = pattern
        hits = re.findall(regexp, query)
        rank += score * len(hits)
    return rank
    

def address_rank(query):
    "takes a list of tokens and determines the likelihood of an address_search"

    buzz_patterns = [
        (3, "\dth"), 
        (3, "\dst"), 
        (3, "\dnd"), 
        (3,  "\drd"), 
        (2, "near"),
        (2, " by "),
        (1, " and "), 
        (1, " & "),
        ]

    return calculate_rank(query, buzz_patterns)

def tag_rank(query):
    "obvious"
    
    patterns = [(5, tag.name.lower()) for tag in models.Tag.objects.all()]

    buzz_patterns = [
        (5, "mexican"),
        (5, "italian"),
        (5, "chinese"),
        (5, "french"),
        (5, "comfort"),
        (5, "soul"),
        (5, "pizza"),
        ]
    return calculate_rank(query, buzz_patterns)
       
def name_rank(query):
    return 3

queries = [query.value for query in models.QueryString.objects.all()]

def rank_summary(query):
    address = (address_rank(query), "address")
    name = (name_rank(query), "name")
    tag = (tag_rank(query), "tag")
    return sorted([address, name, tag], reverse=True)

def summary():
    for query in queries:
        print "query:", query
        print "rank_summary:", rank_summary(query)
        print

summary()
