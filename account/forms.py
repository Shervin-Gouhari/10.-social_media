from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.validators import MinValueValidator, MaxValueValidator


class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(label='', max_value=99999, widget=forms.NumberInput(
        attrs={"aria-required": "true", "placeholder": "Enter your code", "maxlength": "5"}),
        validators=[MinValueValidator(11111), MaxValueValidator(99999)])


class LoginForm(forms.Form):
    phone_number = forms.CharField(label='', max_length=11, widget=forms.TextInput(
        attrs={"aria-required": "true", "placeholder": "Phone number"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={"aria-required": "true", "placeholder": "Password"}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "placeholder": "Enter your email",
            "aria-required": "true", }),
    )


class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        if self.user.check_password(password2):
            return self.add_error('new_password1', 'You have inserted your current password.')
        return password2