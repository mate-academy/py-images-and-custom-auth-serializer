import os.path
import uuid
from django.utils.text import slugify


def movie_img_file_path(instance, filename):
    _, ext = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}.{ext}"

    return os.path.join(
        "uploads",
        "movies",
        filename
    )
