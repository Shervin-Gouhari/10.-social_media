from django.contrib.auth.signals import user_logged_out
from django.contrib import messages


def logout_notifier(sender, request, user, **kwargs):
    messages.success(request, "You are logged out successfully.")


user_logged_out.connect(logout_notifier)
