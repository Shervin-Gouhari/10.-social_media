from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={"aria-required": "true", "placeholder": "Enter your code", "maxlength": "5"}),
        validators=[MinValueValidator(11111), MaxValueValidator(99999)])


class LoginForm(forms.Form):
    phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={"aria-required": "true", "placeholder": "Phone number", "maxlength": "11"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={"aria-required": "true", "placeholder": "Password"}))
