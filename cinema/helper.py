import os
import pathlib
import uuid
from django.utils.text import slugify


def movies_image_path(movie_title: str, filename: str) -> str:
    filename = (
        f"{slugify(movie_title)}-"
        f"{uuid.uuid4()}"
        f"{pathlib.Path(filename).suffix}"
    )
    return os.path.join("upload-image", filename)
