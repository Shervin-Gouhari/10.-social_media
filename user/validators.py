from django.core.exceptions import ValidationError


def username(username):
    if username[0] == '.' or username[0] == '_':
        raise ValidationError(
            (f"Username cannot start with underscore or period."),
            code="username_start_error",
            params={"username": username},
        )
    allowed_characters = 'abcdefghijklmnopqrstuvwxyz1234567890_.'
    for character in username:
        if character not in allowed_characters:
            raise ValidationError(
                (f"You can't include symbols or other punctuation marks as a part of your username."),
                code="username_character_error",
                params={"username": username},
            )
