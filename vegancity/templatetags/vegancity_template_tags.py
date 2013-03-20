from django import template

register = template.Library()

def target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

def nofollow(text):
    return text.replace('<a ', '<a rel="nofollow" ')

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
        else:
            return text.title()
    else:
        return ""

format_search_type = register.filter(format_search_type, is_safe=True)
target_blank = register.filter(target_blank, is_safe=True)
nofollow = register.filter(nofollow, is_safe=True)
showing_vendors_string = register.filter(showing_vendors_string, is_safe=True)
