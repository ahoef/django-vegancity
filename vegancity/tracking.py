# Tracking module
#
# The purpose of this module is to hold functions
# related to tracking.  These are just helper functions
# that have been moved out of the views to reduce the
# complexity of the view code.

import models

def log_query(query, ranks):
    "takes a query and saves it as a querystring object."
    querystring = models.QueryString()
    querystring.value = query
    querystring.rank_results = str(ranks)
    querystring.save()
    
