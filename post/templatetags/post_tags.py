from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def customtimesince(value):
    delta = timesince(value, depth=1)
    return delta
