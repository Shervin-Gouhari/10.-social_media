from django.contrib import messages


def login_required_message(function, message="You have to login first."):
    '''
    if login is required, show an error message.
    (must be used before django's login_required decorator)
    '''
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, message)
        return function(request, *args, **kwargs)
    return wrapper
