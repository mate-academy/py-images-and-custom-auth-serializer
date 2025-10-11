from uuid import uuid4
from pathlib import Path

from django.utils.text import slugify


def create_movie_image_url(instance: str, filename: str) -> str:
    ext = Path(filename).suffix
    path = f"{slugify(instance.title)}-{uuid4().hex}{ext}"

    return str(Path(path))
