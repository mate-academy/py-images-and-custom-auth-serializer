import os
import uuid


def movie_image_path(instance, movie_image: str) -> str:
    split = movie_image.split(".")
    filename, ext = split[0], split[-1]
    return os.path.join("cinema",
                        "movie",
                        f"{filename}{instance.title}-{uuid.uuid4()}.{ext}")
