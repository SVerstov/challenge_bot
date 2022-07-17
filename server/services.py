from . import models


def add_user(**kwargs) -> models.User:
    print(f'add new user @{kwargs["username"]}')
    return models.User.objects.get_or_create(**kwargs)
