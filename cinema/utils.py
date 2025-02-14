import pathlib
import uuid

from django.utils.text import slugify


def custom_movie_image_path(instance, filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/movies/") / pathlib.Path(filename)
