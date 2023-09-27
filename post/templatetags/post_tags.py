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


@register.filter
def human_format(num, method=None):
    if num == 0: return num
    if method == "symbolic":
        magnitude = 0
        while num >= 1000:
            magnitude += 1
            num /= 1000.0
        if str(float(num)).split(".")[1] == str(0):
            return f"{int(num)}{['', 'K', 'M'][magnitude]}"
        return f"{num:.2f}{['', 'K', 'M'][magnitude]}"
    return f"{num:,}"
