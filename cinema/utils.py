from __future__ import annotations
import pathlib
import uuid
from django.utils.text import slugify
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cinema.models import Movie


def movie_image_path(
        instance: Movie, filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/movies/") / pathlib.Path(filename)
