from django import template
from django.utils.timesince import timesince

from datetime import datetime

register = template.Library()


@register.filter
def customtimesince(value):
    if type(value) == str:
        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    delta = timesince(value, depth=1)
    return delta
