import os
import uuid
from slugify import slugify


def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/", f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    )
