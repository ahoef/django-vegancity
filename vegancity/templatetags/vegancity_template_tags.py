import re
from django import template
import hashlib
from urllib import quote_plus

register = template.Library()


def gravatar_urlify(email_address, size=72):
    # TODO: change to something relative or move to settings file
    default = "http://www.vegphilly.com/static/images/default_user_icon.jpg"
    if email_address:
        hash = hashlib.md5(email_address).hexdigest()
        return ("http://gravatar.com/avatar/%s?s=%i&d=%s" %
                (hash, size, quote_plus(default)))
    else:
        return default


def strip_http(text):
    if text:
        text = re.sub('https?://', '', text)
        if text[-1] == '/':
            text = text[:-1]
        return text

strip_http = register.filter(strip_http, is_safe=True)
gravatar_urlify = register.filter(gravatar_urlify, is_safe=True)
