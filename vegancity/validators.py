import re

from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not re.match(r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}', value):
        raise ValidationError(u'phone number must be in the format "(###) ###-####"')
