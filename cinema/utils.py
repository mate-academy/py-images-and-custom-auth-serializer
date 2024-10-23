import os
import pathlib
import uuid

from django.utils.text import slugify


def create_custom_path(instance, filename):
    filename = (f"{slugify(instance.title)}-{uuid.uuid4()}"
                + pathlib.Path(filename).suffix)
    return os.path.join("upload", "movies", filename)
