from django import template

register = template.Library()

def or_none(text):
    if text:
        return text
    else:
        return ""

def target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

def showing_vendors_string(text):
    if text:
        if text == "address":
            return "Showing only food vendors near "
        elif text == "name":
            return "Showing only food vendors with name containing any of "
        else:
            return "Showing only food vendors with tags containing "
    else:
        return ""

or_none = register.filter(or_none, is_safe=True)
target_blank = register.filter(target_blank, is_safe=True)
showing_vendors_string = register.filter(showing_vendors_string, is_safe=True)
