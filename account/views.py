from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from user.models import User
from user.forms import *
from .forms import *


def registration(request):
    data = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.clean_password2():
            user = form.save()
            phone_number = user.phone_number
            request.session['verification_code'] = randint(11111, 99999)
            return redirect(reverse('verification_code', kwargs={'phone_number': phone_number}))
        else:
            messages.error(request, form.errors)
        data = {
            'phone_number': request.POST['phone_number'],
            'username': request.POST['username'],
            'email': request.POST['email']
        }
    return render(request, 'account/registration.html', {'data': data})


def verification_code(request, phone_number):
    print(request.session['verification_code'])
    user = User.objects.get(phone_number=phone_number)
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            if request.session['verification_code'] == form.cleaned_data['verification_code']:
                user.is_active = True
                user.save()
                logout(request)
                login(request, user)
                return redirect(reverse('edit_profile'))
            else:
                messages.error(request, 'false verification code')
        else:
            messages.error(request, form.errors)
    else:
        form = VerificationForm()
    return render(request, 'account/verification_code.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user,
                              data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form})
