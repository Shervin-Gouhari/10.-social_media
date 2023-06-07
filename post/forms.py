from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']


class CommentCreateForm(forms.Form):
    text = forms.CharField(max_length=1000, label="", widget=forms.Textarea(attrs={
        "id": "comment-text-form", "class": "comment-textarea", "placeholder": "Comment here"}))
