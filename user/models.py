from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    email = models.EmailField("email", blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
