from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email_address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
