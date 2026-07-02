import uuid
import os
from django.utils.text import slugify

def movie_image_path(
        instance, filename):
        filename = (
                f"{slugify(instance.title)}-{uuid.uuid4()}"uuid}
        + "
        )) 