from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import PostCreateForm, CommentCreateForm
from .models import Post


@login_required
@require_POST
def post_create(request):
    form = PostCreateForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Post saved successfully.')
    else:
        [messages.error(request, form.errors[error]) for error in form.errors]
    return redirect('profile', request.user)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            form = CommentCreateForm()
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]    
    return render(request, 'post/detail.html', {'post': post, 'form': form})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST['post_id']
    action = request.POST['action']
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            return JsonResponse({'status': 'success'})
        except:
            pass
        return JsonResponse({'status': 'error'})
