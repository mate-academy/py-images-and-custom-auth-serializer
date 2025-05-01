import os
import uuid

from django.utils.text import slugify


def create_custom_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/",
        f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"

    )
