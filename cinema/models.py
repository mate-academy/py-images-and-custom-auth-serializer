import os
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


# 1. Helper function for image path
def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/movies/", filename)


# 2. Update User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# 3. Update Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    # Add the image field
    image = models.ImageField(null=True, upload_to=movie_image_file_path)

    def __str__(self):
        return self.title

# ... other models (Genre, Actor, CinemaHall, MovieSession) ...