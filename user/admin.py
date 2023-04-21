from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from . forms import *


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

        ('Optional Info', {'fields': ('avatar',
         'first_name', 'last_name', 'data_of_birth')}),
    )
    form = UserChangeForm
    fieldsets = (
        ('General Info', {
         'fields': ('avatar', 'phone_number', 'username', 'email', 'password')}),

        ('Personal Info', {
         'fields': ('first_name', 'last_name', 'date_of_birth')}),

        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_admin', 'is_superuser')}),

        ('Additional Info', {'fields': ('date_joined', 'last_login')})
    )
