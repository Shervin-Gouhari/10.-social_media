from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Comment, Reply


@receiver(m2m_changed, sender=Comment.likes.through)
def comment_total_likes(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(m2m_changed, sender=Reply.likes.through)
def reply_total_likes(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()
    
    