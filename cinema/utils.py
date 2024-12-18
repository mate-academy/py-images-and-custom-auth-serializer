import pathlib
from uuid import uuid4

from django.utils.text import slugify



def movie_image_path(instance: "Movie", filename: str) -> pathlib.Path: # noqa
    filename = (
        f"{slugify(instance.title)}-{uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload-image/") / pathlib.Path(filename)
