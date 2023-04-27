from random import randint

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
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            if request.session['verification_code'] == form.cleaned_data['verification_code']:
                unsaved_user['is_active'] = True
                if unsaved_user['id'] == None:
                    user = User.objects.create(**unsaved_user)
                    logout(request)
                    login(request, user)
                else:
                    User.objects.get(id=unsaved_user['id']).update(**unsaved_user)
                del request.session['unsaved_user']
                return redirect(reverse('edit_profile'))
            else:
                messages.error(request, 'False verification code.')
        else:
            messages.error(request, form.errors)
    else:
        request.session['verification_code'] = randint(11111, 99999)
        ver_code = request.session['verification_code']
        send_sms(request, unsaved_user['phone_number'], ver_code)
        form = VerificationForm()
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
            request.user.avatar = form.cleaned_data.get('avatar', request.user.avatar)
            request.user.save(update_fields=["avatar"])
            if phone_number != form.cleaned_data['phone_number']:
                request.user.is_active = False
                unsaved_user = form.save(commit=False)
                exclude = ['avatar', 'password']
                request.session['unsaved_user'] = model_to_dict(unsaved_user, exclude=exclude)
                return redirect(reverse('verification_code'))
            else:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect(reverse('profile'))
        else:
            messages.error(request, form.errors)
    return render(request, 'account/edit_profile.html', {'form': form})
