import re
import urllib2

from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not re.match(r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}', value):
        raise ValidationError(u'phone number must be in the format "(###) ###-####"')

def validate_website(value):
    print "value:", value
    print type(value)
    try:
        urllib2.urlopen(value)
    except urllib2.URLError:
        raise ValidationError(u'That url appears not to work.')
