from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'username',
                  'email', 'first_name', 'last_name']
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    password = ReadOnlyPasswordHashField()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['-date_joined']
    search_fields = ['phone_number', 'username', 'email']
    filter_horizontal = ()
    readonly_fields = ['date_joined', 'last_login']

    list_display = ['phone_number', 'username', 'email', 'first_name',
                    'last_name', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_admin', 'is_superuser']

    add_form = UserCreationForm
    add_fieldsets = (
        ('Mandatory Info', {'fields': ('phone_number',
         'username', 'email', 'password1', 'password2')}),

        ('Optional Info', {'fields': ('first_name', 'last_name')}),
    )
    form = UserChangeForm
    fieldsets = (
        ('General Info', {
         'fields': ('phone_number', 'username', 'email', 'password')}),

        ('Personal Info', {'fields': ('first_name', 'last_name')}),

        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_admin', 'is_superuser')}),

        ('Additional Info', {'fields': ('date_joined', 'last_login')})
    )
