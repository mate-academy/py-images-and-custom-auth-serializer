from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,
                    **extra):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,
                         password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get("is_staff") is not True:
            raise ValueError("Superuser "
                             "must have is_staff=True.")
        if extra.get("is_superuser") is not True:
            raise ValueError("Superuser must have "
                             "is_superuser=True.")
        return self.create_user(email, password, **extra)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
