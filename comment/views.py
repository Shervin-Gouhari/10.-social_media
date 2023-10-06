from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from account.decorators import login_required_message
from .models import Comment


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

