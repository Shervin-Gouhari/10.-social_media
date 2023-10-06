from django.db import models
from django.conf import settings

from post.models import Post


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
        
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited = models.DateTimeField(auto_now=True)
    total_likes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.user} {self.created}'
    
    
class Reply(models.Model):
    class Meta:
        db_table = 'reply'
        
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reply_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited = models.DateTimeField(auto_now=True)
    total_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user} {self.created}'
    
