from django.core.exceptions import ValidationError


def username_validator(username):
    if username[0] == '.' or username[0] == '_':
        raise ValidationError("Username cannot start with underscore or period.")
    allowed_characters = 'abcdefghijklmnopqrstuvwxyz1234567890_.'
    for character in username:
        if character not in allowed_characters:
            raise ValidationError("You can't include symbols or other punctuation marks as a part of your username.")
