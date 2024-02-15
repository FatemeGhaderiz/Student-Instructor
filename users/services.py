from django.db import transaction
from .models import BaseUser


def create_user(*, email: str, username: str, password: str):
    return BaseUser.objects.create_user(
        email=email, username=username, password=password
    )


@transaction.atomic
def register(email: str, username: str, password: str):

    user = create_user(email=email, username=username, password=password)
    return user
