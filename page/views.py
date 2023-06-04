from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import User
from post.models import Post
from action.models import Action


@login_required
def home(request):
    user_posts = Post.objects.filter(user=request.user)
    friend_posts = Post.objects.none()
    for friend in request.user.following.all():
        friend_posts |= Post.objects.filter(user=friend)
    total_posts = (user_posts | friend_posts).order_by("-created")
    paginator = Paginator(total_posts, 4)
    page = request.GET.get("page", None)
    if page:
        try:
            posts_orderByCreationAscending = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            return JsonResponse({"response": "failure"})
        return JsonResponse({"response": render_to_string("account/loader/post/home.html", {"posts_orderByCreationAscending": posts_orderByCreationAscending}, request=request)})
    
    actions = Action.objects.exclude(user=request.user)
    friends_ids = request.user.following.values_list("id", flat=True)
    actions = actions.filter(user_id__in=friends_ids).order_by("-created")[:10]
    
    friends = User.objects.filter(id__in=friends_ids)
    suggestion_list = User.objects.none()
    for friend in friends:
        for suggestion in friend.following.all():
            if suggestion != request.user and suggestion not in friends:
                suggestion = User.objects.filter(id=suggestion.id)
                suggestion_list |= suggestion
    
    context = {"posts_orderByCreationAscending": paginator.page(1),
               "actions": actions,
               "suggestion_list": suggestion_list[:5]}
    return render(request, "page/home.html", context)


def explore(request):
    posts = Post.objects.order_by("-likes")
    return render(request, "page/explore.html", {"posts": posts})