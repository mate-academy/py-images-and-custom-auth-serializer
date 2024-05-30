import pathlib
import uuid

from django.utils.text import slugify


def movie_image_path(instance, filename) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}--{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("movies/") / pathlib.Path(filename)
