from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class EmailUserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        if not email:
            raise ValueError("User must have an email address")

        if not password:
            raise ValueError("User must have password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email=email, password=password)

        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=255, verbose_name="email address", unique=True)
    username = None
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmailUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
