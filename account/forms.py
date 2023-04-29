from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(
        validators=[MinValueValidator(11111), MaxValueValidator(99999)])


class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
