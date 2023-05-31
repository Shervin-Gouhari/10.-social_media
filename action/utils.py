from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action

import datetime


def action_create(user, act, target):
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    target_ct = ContentType.objects.get_for_model(target)
    similar_actions = Action.objects.filter(user=user, target_ct=target_ct, target_id=target.id, created__gte=last_minute)
    if not similar_actions:
        Action.objects.create(user=user, act=act, target=target)
        return True
    return False