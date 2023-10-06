from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http.response import Http404

from account.decorators import login_required_message
from .models import Comment, Reply


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


# @login_required_message
# @login_required
# def comment_delete(request, id):
#     try:
#         comment = get_object_or_404(Comment, id=id)
#     except Http404:
#         comment = get_object_or_404(Reply, id=id)
#     if request.method == "POST":
#         comment.delete()
#         return JsonResponse({"status": "success"})
#     return JsonResponse({"response": render_to_string("loader/comment_delete.html", {"comment": comment}, request=request)})

