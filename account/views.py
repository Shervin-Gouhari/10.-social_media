from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


@login_required
def profile(request):
    return render(request, 'account/profile.html')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
