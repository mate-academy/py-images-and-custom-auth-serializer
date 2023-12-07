import os
import uuid

from django.utils.text import slugify


def img_directory_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "upload-image/",
        f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    )
