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

def log_query(query, ranks):
    "takes a query and saves it as a querystring object."
    querystring = models.QueryString()
    querystring.body = query
    querystring.ranking_summary = str(ranks)
    querystring.save()
    
