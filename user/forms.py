from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import User



class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'email']
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data['password2']
        user = super().save(commit=False)
        if password != '':
            user.set_password(password)
        if commit:
            user.save()
        return user



class UserChangeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'biography']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date(), 'min': datetime(1920, 1, 1).date()})
            }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "leave empty, if you don't wish to change"}), required=False)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={"placeholder": "leave empty, if you don't wish to change"}), required=False)
