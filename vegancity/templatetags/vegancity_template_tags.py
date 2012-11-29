from django import template

register = template.Library()

def target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

target_blank = register.filter(target_blank, is_safe=True)
