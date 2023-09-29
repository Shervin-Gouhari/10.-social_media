from django import forms
from .models import Post, Media, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'location']
        widgets = {
            'caption': forms.Textarea(attrs={'placeholder': 'Caption...', 'rows': '10', 'maxlength': '2000'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location', 'maxlength': '50'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class MediaCreateForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media']

    media = forms.FileField(label="", widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'accept': '.jpeg, .jpg, .png, .mkv, .mp4', 'aria-required': 'true'}))


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(max_length=1000, label="", widget=forms.Textarea(attrs={
        "id": "comment-text-form", "class": "comment-textarea", "placeholder": "Comment here"}))
