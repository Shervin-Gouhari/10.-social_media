from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

from smart_selects.db_fields import ChainedForeignKey

from .validators import username


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, email, password=None):
        if not phone_number:
            raise ValueError("phone number is required")
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email, password=None):
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default='avatar/default.jpg')
    phone_number = models.CharField(max_length=11, unique=True, validators=[RegexValidator(regex="\A(09)(0|1|2|3)[0-9]{7}\d\Z", message='Incorrect phone number.')])
    username = models.CharField(max_length=30, unique=True, validators=[username])
    email = models.EmailField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.CASCADE, null=True, blank=True) 
    city = ChainedForeignKey('cities_light.City', chained_field="country", chained_model_field="country", show_all=False, sort=True, on_delete=models.CASCADE, null=True, blank=True)
    biography = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    following = models.ManyToManyField("self", through="Contact", related_name="followers", symmetrical=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="rel_to_set", on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
