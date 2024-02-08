from ..models import Course
from users.models import BaseUser

from django.db import transaction
from django.utils.text import slugify


@transaction.atomic
def create_course(*, instructor: BaseUser, title: str, category: str , is_public:bool):
     

     course =Course.objects.create(
        instructor=instructor, title=title, category=category, slug=slugify(title), is_public=is_public
    )
     return course