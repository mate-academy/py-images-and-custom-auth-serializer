import os
import uuid

from django.utils.text import slugify


def movie_image_path(instance, movie_image: str) -> str:
    split = movie_image.split(".")
    _, ext = split[0], split[-1]
    return os.path.join("upload",
                        "movies",
                        f"{slugify(instance.title)}-{uuid.uuid4()}.{ext}")
