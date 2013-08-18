import re
import urllib2

from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not re.match(r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}', value):
        raise ValidationError(u'phone number must be in the format "(###) ###-####"')

def validate_website(value):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.95 Safari/537.11'}
        req = urllib2.Request(value, None, headers)
        urllib2.urlopen(req)
    except urllib2.URLError:
        raise ValidationError(u'That url appears not to work.')
