from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
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
            unsaved_user = form.save(commit=False)
            request.session['unsaved_user'] = model_to_dict(unsaved_user, exclude='avatar')
            return redirect(reverse('verification_code'))
        else:
            messages.error(request, form.errors)
        data = {
            'phone_number': request.POST['phone_number'],
            'username': request.POST['username'],
            'email': request.POST['email']
        }
    return render(request, 'account/registration.html', {'data': data})


def verification_code(request):
    unsaved_user = request.session['unsaved_user']
    ver_code = send_sms(request, unsaved_user['phone_number'])
    form = VerificationForm()
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            if ver_code == form.cleaned_data['verification_code']:
                unsaved_user['is_active'] = True
                user = User.objects.create(**unsaved_user)
                del request.session['unsaved_user']
                logout(request)
                login(request, user)
                return redirect(reverse('edit_profile'))
            else:
                messages.error(request, 'False verification code.')
        else:
            messages.error(request, form.errors)
    return render(request, 'account/verification_code.html', {'form': form})


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
            if phone_number != form.cleaned_data['phone_number']:
                request.user.is_active = False
                user = form.save()
                phone_number = user.phone_number
                return redirect(reverse('verification_code', kwargs={'phone_number': phone_number}))
            else:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect(reverse('profile'))
        else:
            messages.error(request, form.errors)
    return render(request, 'account/edit_profile.html', {'form': form})
