from random import randint

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from user.models import User
from user.forms import *
from .forms import *
from .kavenegar import send_sms


def registration(request):
    data = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.clean_password2():
            new_user = form.save(commit=False)
            request.session['new_user'] = model_to_dict(new_user, exclude='avatar')
            return redirect('verification_code')
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]
        data = {
            'phone_number': request.POST['phone_number'],
            'username': request.POST['username'],
            'email': request.POST['email']
        }
    return render(request, 'account/registration.html', {'data': data})


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
                else:
                    user = User.objects.get(id=new_user['id'])
                    setattr(user, 'phone_number', new_user['new_num'])
                    user.save()
                    del request.session['new_user']
                    messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile')
            else:
                messages.error(request, 'False verification code.')
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]
    else:
        request.session['verification_code'] = randint(11111, 99999)
        ver_code = request.session['verification_code']
        send_sms(request, new_user['phone_number'], ver_code)
        form = VerificationForm()
    return render(request, 'account/verification_code.html', {'form': form})


def custom_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in successfully.")
                return redirect("pages:home")
            else:
                messages.error(request, "No user found with said credentials.")
    else:
        if request.user.is_authenticated:
            logout(request)
    return render(request, 'registration/login.html', {'form':form})


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
def edit_profile(request):
    form = UserChangeForm(instance=request.user)
    del form.fields['password']
    if request.method == 'POST':
        phone_number = request.user.phone_number
        form = UserChangeForm(instance=request.user,
                              data=request.POST, files=request.FILES)
        if form.is_valid():
            update_fields = ['avatar', 'username', 'email','first_name', 'last_name', 'date_of_birth', 'biography']
            user = form.save(commit=False)
            user.save(update_fields=update_fields)
            if phone_number != form.cleaned_data['phone_number']:
                new_user = {
                    'id': request.user.id,
                    'is_active': False,
                    'phone_number': phone_number,
                    'new_num': form.cleaned_data['phone_number']}
                request.session['new_user'] = new_user
                return redirect('verification_code')
            else:
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
        else:
            [messages.error(request, form.errors[error]) for error in form.errors]
    return render(request, 'account/edit_profile.html', {'form': form})
