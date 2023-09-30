from django.core.exceptions import ValidationError


def file_size_validator(file):
    if file.size > 10**8:  
        raise ValidationError("Files cannot be larger than 100MB.")
