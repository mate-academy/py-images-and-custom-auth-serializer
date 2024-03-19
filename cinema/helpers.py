import pathlib
import uuid

from django.utils.text import slugify


def create_custom_path(instance, filename) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}-"
        f"{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    )
    return pathlib.Path("uploads/movies/") / pathlib.Path(filename)
