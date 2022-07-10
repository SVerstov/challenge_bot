from . import models


# def add_user(user_id: int, username: str, first_name: str, last_name: str, language_code: str) -> models.User:
#     print(f'add new user @{username}')
#     return models.User.objects.get_or_create(
#         user_id=user_id, username=username, first_name=first_name, last_name=last_name, language_code=language_code
#     )


def add_user(**kwargs) -> models.User:
    print(f'add new user @{kwargs["username"]}')
    return models.User.objects.get_or_create(**kwargs)


