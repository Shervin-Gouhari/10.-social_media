from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework.views import APIView

from action.utils import action_create
from account.decorators import login_required_message
from .forms import PostCreateForm, MediaCreateForm, CommentCreateForm
from .models import Post, Comment
from .serializers import CommentSerializer


@login_required_message
@login_required
def post_create(request):
    if request.method == "POST":
        post_form = PostCreateForm(data=request.POST)
        media_form = MediaCreateForm(files=request.FILES)
        files = request.FILES.getlist('media')
        
        if post_form.is_valid() and media_form.has_clean_media(files):
            post = post_form.save(commit=False)
            post.user = request.user
            
            cleaned_data = []
            for file in files:
                media_form = MediaCreateForm(files={'media': file})
                if media_form.is_valid():
                    cleaned_data.append(media_form)
                else:
                    [messages.error(request, media_form.errors[error]) for error in media_form.errors]    
                    return redirect('profile', request.user)
            
            post.save()
            for clean_data in cleaned_data:
                media = clean_data.save(commit=False)
                media.post = post
                media.save()
            action_create(request.user, "posted", post)
            messages.success(request, 'Post saved successfully.')
        else:
            [messages.error(request, post_form.errors[error]) for error in post_form.errors]
            [messages.error(request, media_form.errors[error]) for error in media_form.errors]
        return redirect('profile', request.user)
    else:
        post_form, media_form = PostCreateForm(), MediaCreateForm()
        response = render_to_string("loader/post_create.html", {"post_form": post_form, "media_form": media_form}, request=request)
        return JsonResponse({"response": response})


@login_required_message
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect('profile', request.user)
    return JsonResponse({"response": render_to_string("loader/post_delete.html", {"post": post}, request=request)})


@login_required_message
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostCreateForm(data=request.POST, instance=post)
        if form.is_valid():
            if post.is_edited == False:
                post.is_edited = True
                post.save()
            form.save()
            return redirect('post:detail', slug)
    form = PostCreateForm(initial=post.__dict__)
    return JsonResponse({"response": render_to_string("loader/post_edit.html", {"post": post, "form": form}, request=request)})
    

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments_orderByCreationAscending = post.comments.order_by("-created", "-total_likes")
    comments_orderByLikesAscending = post.comments.order_by("-total_likes", "-created")
    form = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                response = render_to_string("loader/post_detail.html", {"cm": comment}, request=request)
                return JsonResponse({'status': 'success', 'response': response})
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
            a = post.comments.order_by("-created", "-total_likes")
            aa = CommentSerializer(instance=a, many=True, context={'request': request}).data
            context = {'comments': aa}
        elif by == 'comments_orderByLikesAscending':
            b = post.comments.order_by("-total_likes", "-created")
            bb = CommentSerializer(instance=b, many=True, context={'request': request}).data
            context = {'comments': bb}
        else:
            return JsonResponse({'status': 'failure'})
        response = render_to_string("loader/PostDetailAPI.html", context, request=request)
        return JsonResponse({'status': 'success', 'response': response})


@login_required_message
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
        
     
@login_required_message   
@login_required
@require_POST
def post_save(request):
    post_id = request.POST.get('post_id', None)
    post_action = request.POST.get('post_action', None)
    if post_id and post_action:
        try:
            post = Post.objects.get(id=post_id)
            if post_action == 'save':
                post.saves.add(request.user)
            else:
                post.saves.remove(request.user)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failure'}) 


@login_required_message
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
