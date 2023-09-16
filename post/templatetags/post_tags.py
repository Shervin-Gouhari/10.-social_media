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


@register.filter
def extension(value):
    supported_image_extensions = ['jpeg', 'jpg', 'png']
    supported_video_extensions = ['mkv', 'mp4']
    extension = str(value.media).split('.')[-1].lower()
    if extension in supported_image_extensions:
        return 'image'
    elif extension in supported_video_extensions:
        return 'video'
    