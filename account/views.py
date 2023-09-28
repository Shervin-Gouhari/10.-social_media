from random import randint

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.http import JsonResponse

from user.models import User, Contact
from user.forms import *
from post.models import Post
from action.utils import action_create

from .forms import *
from .utils import send_sms, send_mail


def registration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.clean_password2():
            new_user = form.save(commit=False)
            request.session['new_user'] = model_to_dict(new_user, exclude=['avatar', 'following'])
            return redirect('verification_code')
    return render(request, 'account/registration.html', {'form': form})


def verification_code(request):
    new_user = request.session['new_user']
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            if request.session['verification_code'] == form.cleaned_data['verification_code']:
                new_user['is_active'] = True
                if new_user['id'] == None:
                    user = User.objects.create(**new_user)
                    del request.session['new_user']
                    logout(request)
                    login(request, user)
                    messages.success(request, 'Profile created successfully.')
                    send_mail(user)
                else:
                    user = User.objects.get(id=new_user['id'])
                    setattr(user, 'phone_number', new_user['new_num'])
                    user.save()
                    del request.session['new_user']
                    messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile', user)
            else:
                messages.error(request, 'False verification code.')
    else:
        request.session['verification_code'] = randint(11111, 99999)
        ver_code = request.session['verification_code']
        send_sms(request, new_user['phone_number'], ver_code)
        form = VerificationForm()
    return render(request, 'account/verification_code.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logout(request)
                login(request, user)
                messages.success(request, "You are logged in successfully.")
                return redirect("page:home")
            else:
                messages.error(request, "No user found with said credentials.")
    return render(request, 'registration/login.html', {"form": form})


class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    
    
class PasswordResetConfirm(PasswordResetConfirmView):
    post_reset_login = True
    success_url = reverse_lazy("page:home")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password reset successfully.")
        return response
     
    
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by("-created")
    paginator = Paginator(posts, 6)
    page = request.GET.get("page", None)
    if page:
        try:
            posts_orderByCreationAscending = paginator.page(page)
        except(EmptyPage, PageNotAnInteger):
            return JsonResponse({"response": "failure"})
        return JsonResponse({"response": render_to_string("loader/post/profile.html", {"posts_orderByCreationAscending": posts_orderByCreationAscending}, request=request)}) 
    context = {"user": user,
               "posts_orderByCreationAscending": paginator.page(1)}
    return render(request, 'account/profile.html', context)


@login_required
def edit_profile(request, username):
    form = UserChangeForm(instance=request.user)
    if request.method == 'POST':
        phone_number = request.user.phone_number
        form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password2']
            update_fields = ['avatar', 'username', 'email','first_name', 'last_name', 'date_of_birth', 'biography', 'password']
            if password != '': form.clean_password2()
            user = form.save(commit=False)
            user.save(update_fields=update_fields)
            if password != '': login(request, user)
            if phone_number != form.cleaned_data['phone_number']:
                new_user = {
                    'id': user.id,
                    'is_active': False,
                    'phone_number': phone_number,
                    'new_num': form.cleaned_data['phone_number']}
                request.session['new_user'] = new_user
                return redirect('verification_code')
            else:
                messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile', user)
    return render(request, 'account/edit_profile.html', {'form': form})


@login_required
@require_POST
def follow(request):
    user_id = request.POST.get("user_id", None)
    user_action = request.POST.get("user_action", None)
    if user_id and user_action:
        try:
            user = User.objects.get(id=user_id)
            if user_action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                action_create(request.user, "followed", user)
            else:
                Contact.objects.get(user_from=request.user, user_to=user).delete()
                action_create(request.user, "unfollowed", user)
            return JsonResponse({"status": "success"})
        except:
            pass
    return JsonResponse({"status": "failure"})


@require_GET
def search(request):
    query = request.GET.get('query', None)
    if query:
        search_result = User.objects.filter(username__icontains=query)
        return JsonResponse({"response": render_to_string("loader/search.html", {"search_result": search_result}, request=request)})
    return JsonResponse({"response": "failure"})
