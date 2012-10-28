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



# Tracking module
#
# The purpose of this module is to hold functions
# related to tracking.  These are just helper functions
# that have been moved out of the views to reduce the
# complexity of the view code.

import models
import redis
import settings

def log_query(query, ranks):
    "takes a query and saves it in a redis store."

    #TODO: better error handling
    try:
        serv = redis.Redis(settings.REDIS_SERVER)
        this_app = settings.REDIS_APPNAME
        
        # add query to the list of queries for this app
        key_list = this_app + "_querystrings"
        serv.rpush(key_list, query)

        serv.set(query, str(ranks))
    except:
        pass


def get_log():

    #TODO: better error handling
    try:
        serv = redis.Redis(settings.REDIS_SERVER)
        this_app = settings.REDIS_APPNAME

        key_list = serv.lrange(this_app + "_querystrings", 0, -1)
    
        results = []
        for key in key_list:
            results.append((key, serv.get(key)))

        return results
    except:
        return None
                       
