from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework.views import APIView

from action.utils import action_create
from .forms import PostCreateForm, CommentCreateForm
from .models import Post, Comment
from .serializers import CommentSerializer


@login_required
@require_POST
def post_create(request):
    form = PostCreateForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        action_create(request.user, "posted", post)
        messages.success(request, 'Post saved successfully.')
    else:
        [messages.error(request, form.errors[error]) for error in form.errors]
    return redirect('profile', request.user)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments_orderByCreationAscending = post.comments.all().order_by("-created", "-likes")
    comments_orderByLikesAscending = post.comments.all().order_by("-likes", "-created")
    form = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return JsonResponse({'status': 'success',
                                     "newCommentId": comment.id})
            except:
                return JsonResponse({'status': 'failure'})
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]
    context = {'post': post,
               'form': form,
               'comments_orderByCreationAscending': comments_orderByCreationAscending,
               'comments_orderByLikesAscending': comments_orderByLikesAscending}
    return render(request, 'post/detail.html', context)


class PostDetailAPI(APIView):
    def get(self, request, slug):
        by = request.GET.get('by', None)
        post = get_object_or_404(Post, slug=slug)
        if by == 'comments_orderByCreationAscending':
            a = post.comments.all().order_by("-created", "-likes")
            aa = CommentSerializer(instance=a, many=True, context={'request': request}).data
            context = {'comments': aa}
        elif by == 'comments_orderByLikesAscending':
            b = post.comments.all().order_by("-likes", "-created")
            bb = CommentSerializer(instance=b, many=True, context={'request': request}).data
            context = {'comments': bb}
        else:
            return JsonResponse({'status': 'failure'})
        response = render_to_string("account/loader/comment/detail.html", context, request=request)
        return JsonResponse({'status': 'success', 'response': response})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('post_id', None)
    post_action = request.POST.get('post_action', None)
    if post_id and post_action:
        try:
            post = Post.objects.get(id=post_id)
            if post_action == 'like':
                post.likes.add(request.user)
                action_create(request.user, "liked", post)
            else:
                post.likes.remove(request.user)
                action_create(request.user, "disliked", post)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failure'}) 


@login_required
@require_POST
def comment_like(request):
    comment_id = request.POST.get('comment_id', None)
    comment_action = request.POST.get('comment_action', None)
    if comment_id and comment_action:
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment_action == 'like':
                comment.likes.add(request.user)
            else:
                comment.likes.remove(request.user)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failure'})    
