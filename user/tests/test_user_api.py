from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)
