import re
import hashlib

from urllib import quote_plus

from django import template
from django.conf import settings

DEFAULT_USER_ICON = quote_plus(
    "http://%s/static/images/default_user_icon.jpg" % settings.HOSTNAME)

def gravatar_urlify(email_address, size=72):
    if email_address:
        hash = hashlib.md5(email_address).hexdigest()
        return ("http://gravatar.com/avatar/%s?s=%i&d=%s" %
                (hash, size, DEFAULT_USER_ICON))
    else:
        return DEFAULT_USER_ICON


def strip_http(text):
    if text:
        text = re.sub('https?://', '', text)
        if text[-1] == '/':
            text = text[:-1]
        return text

register = template.Library()
strip_http = register.filter(strip_http, is_safe=True)
gravatar_urlify = register.filter(gravatar_urlify, is_safe=True)
