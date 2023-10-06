from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['post', 'user', 'created', 'is_edited', 'edited']
    list_filter = ['created', 'edited']
    search_fields = ['id']

