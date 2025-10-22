from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

REGISTRATION_CHOICES = [
    ('email', 'Email'),
    ('google', 'Google')
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, help_text="The user's unique email address.")
    first_name = models.CharField(max_length=30, default='', null=True, blank=True, help_text="The user's first name.")
    last_name = models.CharField(max_length=30, default='', null=True, blank=True, help_text="The user's last name.")

    registration_method = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default='email')

    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, help_text="Indicates whether the user has all admin permissions. Defaults to False.")
    is_active = models.BooleanField(default=False, help_text="Indicates whether the user account is active. Defaults to False and user needs to verify email on signup before it can be set to True.")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user joined.")
    
    def __str__(self):
        return self.email

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
