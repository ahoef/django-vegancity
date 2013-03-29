import re
from django import template

register = template.Library()

def showing_vendors_string(text):
    if text:
        if text == "address":
            return " near "
        elif text == "name":
            return " with name containing any of "
        else:
            return " with cuisine or features containing any of "
    else:
        return ""

def format_search_type(text):
    if text:
        if text == "tag":
            return "Cuisine & Features"
        elif text == "address":
            return "Location"
        else:
            return text.title()
    else:
        return ""

def format_button_title(text):
    if text == "location":
        return "Enter an address, intersection or zip code"
    else:
        return ""

def strip_http(text):
    if text:
        text = re.sub('https?://', '', text)
        if text[-1] == '/':
            text = text[:-1]
        return text

format_search_type = register.filter(format_search_type, is_safe=True)
format_button_title = register.filter(format_button_title, is_safe=True)
showing_vendors_string = register.filter(showing_vendors_string, is_safe=True)
strip_http = register.filter(strip_http, is_safe=True)
