# module for performing various sorts of geocoding related tasks

import math
import urllib
import json

from settings import LOCATION_LATITUDE, LOCATION_CITY_STATE

def geocode_address(address):
    "takes an address as a string and returns a tuple of latitude and longitude in float format"

    address = address + " " + LOCATION_CITY_STATE
    base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    address_param = "address=" + urllib.quote_plus(address)
    sensor_param = "sensor=false"
    full_url = base_url + address_param + "&" + sensor_param
    raw_response = urllib.urlopen(full_url).read()
    json_response = json.loads(raw_response)
    if not json_response['status'] == 'OK':
        return None
    else:
        latitude = json_response['results'][0]['geometry']['location']['lat']
        longitude = json_response['results'][0]['geometry']['location']['lng']
    return latitude, longitude


def sign_multiple(num):
    "returns -1 if a number is negative, else 1"
    if num >= 0:
        return 1
    else:
        return -1


def distances(origin, points):

    base_url = "http://maps.googleapis.com/maps/api/distancematrix/json?mode=bicycling&units=imperial&"

    origin_string = "%f,%f" % origin
    origin_param = "origins=" + origin_string

    destinations_tokens = ["%f,%f" % point for point in points]
    destinations_string = "|".join(destinations_tokens)
    destinations_param = "destinations=" + destinations_string

    sensor_param = "sensor=false"

    full_url = base_url + origin_param + "&" + destinations_param + "&" + sensor_param

    raw_response = urllib.urlopen(full_url).read()
    json_response = json.loads(raw_response)
    if not json_response['status'] == 'OK':
        return None
    else:
        # return a list of distance descriptions and values in feet
        return [(hash['distance']['text'], hash['distance']['value']) 
                for hash in json_response['rows'][0]['elements']]


def meters_to_miles(m):
    return m * 0.000621371
    

def bounding_box_offsets(point, distance):
    """takes a point and a distance and returns
    a latitude offset and a longitude offset
    that will produce an approximate bounding
    box."""

    latitude, longitude = point

    latitude_offset = distance / 69.172
    longitude_offset = abs(distance / (69.172 * math.cos(LOCATION_LATITUDE)))

    latitude_ceiling = sign_multiple(latitude) * abs((latitude) + (latitude_offset))
    latitude_floor = sign_multiple(latitude) * abs((latitude) - (latitude_offset))
    longitude_ceiling = sign_multiple(longitude) * abs((longitude) + (longitude_offset))
    longitude_floor = sign_multiple(longitude) * abs((longitude) - (longitude_offset))
    return latitude_floor, latitude_ceiling, longitude_floor, longitude_ceiling
