from datetime import datetime

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from .validators import file_size_validator


class Post(models.Model):
    class Meta:
        db_table = 'post'
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Save', blank=True)
    caption = models.TextField(max_length=2000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    total_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'({self.user} {self.created})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user} {datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})
    
    
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media = models.FileField(upload_to='posts/%Y/%m/%d', validators=[FileExtensionValidator(['jpeg', 'jpg', 'png', 'mkv', 'mp4']), file_size_validator])
    
    def __str__(self):
        return f'{self.media} in {self.post}'
    
    
class Save(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_saves", on_delete=models.CASCADE)
    post_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user_from} saved {self.post_to}'
    
    
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
    