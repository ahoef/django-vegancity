# module for performing various sorts of geocoding related tasks

import urllib
import json

def geocode_address(address):
    "takes an address as a string and returns a tuple of latitude and longitude in float format"

    base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    address_param = "address=" + urllib.quote_plus(address)
    sensor_param = "&sensor=false"
    full_url = base_url + address_param + sensor_param
    raw_response = urllib.urlopen(full_url).read()
    json_response = json.loads(raw_response)
    if not json_response['status'] == 'OK':
        return None
    else:
        latitude = json_response['results'][0]['geometry']['location']['lat']
        longitude = json_response['results'][0]['geometry']['location']['lng']
    return latitude, longitude
