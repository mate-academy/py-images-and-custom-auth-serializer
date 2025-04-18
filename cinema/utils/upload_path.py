import os
import uuid
from django.utils.text import slugify


def movie_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"

    return f"uploads/movies/{filename}"
