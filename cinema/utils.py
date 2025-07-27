from django.utils.text import slugify
import pathlib
import uuid


def movie_image_path(instance, filename: str) -> pathlib.Path:
    filename = (f"{slugify(instance.title)}-{uuid.uuid4()}"
                + pathlib.Path(filename).suffix)
    return pathlib.Path("upload/movies/") / pathlib.Path(filename)
