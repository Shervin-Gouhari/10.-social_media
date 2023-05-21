from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import PostCreateForm
from .models import Post


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post saved successfully.')
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]     
    else:
        messages.error(request, 'GET requests not allowed.')
    return redirect('profile', request.user)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post/detail.html', {'post': post})
        
