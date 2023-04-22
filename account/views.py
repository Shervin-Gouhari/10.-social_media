from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.forms import *


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.clean_password2():
            form.save()
            return redirect(reverse('login'))
        else:
            messages.error(request, 'passwords do not match')
    else:
        form = UserCreationForm()
    return render(request, 'account/registration.html', {'form': form})


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
