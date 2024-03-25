import os
import uuid

from django.utils.text import slugify


def movie_image_file_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"

    return os.path.join("uploads/movies/", filename)
