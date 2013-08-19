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

""" module for performing various sorts of geocoding related tasks """

import urllib
import json

from settings import LOCATION_BOUNDS, LOCATION_COMPONENTS


def geocode_address(address):
    """takes an address as a string and returns a tuple of latitude,
    longitude and neighborhood in float format"""
    base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    address_param = "address=" + urllib.quote_plus(address)
    sensor_param = "sensor=false"
    bounds_param = "bounds=" + LOCATION_BOUNDS
    components_param = "components=" + LOCATION_COMPONENTS

    full_url = base_url + "&".join([address_param, sensor_param,
                                    bounds_param, components_param])
    raw_response = urllib.urlopen(full_url).read()
    json_response = json.loads(raw_response)
    if not json_response['status'] == 'OK':
        return None
    else:
        latitude = json_response['results'][0]['geometry']['location']['lat']
        longitude = json_response['results'][0]['geometry']['location']['lng']
        neighborhd_hashes = [hash for hash in
                             json_response['results'][0]['address_components']
                             if 'neighborhood' in hash['types']]
        if neighborhd_hashes:
            neighborhood = neighborhd_hashes[0]['long_name']
        else:
            neighborhood = None
    return latitude, longitude, neighborhood
