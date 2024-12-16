import os
import uuid

from django.utils.text import slugify


class CustomMediaPath:
    """
    Utility class for generating custom
    file paths for uploaded media files.
    """
    @staticmethod
    def create_custom_path(instance, filename: str):
        _, extension = os.path.splitext(filename)
        return os.path.join(
            "uploads/images/",
            f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
        )
