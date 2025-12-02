from django.contrib.auth.models import (AbstractUser,
                                        UserManager as DjangoUserManager)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(DjangoUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new `User` with an email, password"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model"""

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
