from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['user', 'created', 'is_edited', 'edited']
    list_filter = ['created', 'edited']
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['post', 'user', 'created', 'is_edited', 'edited']
    list_filter = ['created', 'edited']
