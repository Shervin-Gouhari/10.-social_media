from datetime import datetime

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(max_length=2000, blank=True)
    location = models.CharField(max_length=50, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    total_likes = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f'{self.user} {self.created}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user} {datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})
    
    
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media = models.FileField(upload_to='posts/%Y/%m/%d')
    
    
class Comment(models.Model):
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