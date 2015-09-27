__author__ = 'chirag'
from django.template.defaultfilters import register

@register.filter
def lookup(d, key_name):
    return d[str(key_name)]