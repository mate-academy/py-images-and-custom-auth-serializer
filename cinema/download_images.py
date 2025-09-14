import pathlib
import uuid

from django.utils.text import slugify


def movie_image_path(instance, filename: str) -> str:
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return str(pathlib.Path("upload/movies/") / pathlib.Path(filename))
