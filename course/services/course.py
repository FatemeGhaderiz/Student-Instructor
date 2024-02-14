from ..models import Course
from users.models import BaseUser

from django.db import transaction
from django.utils.text import slugify



def create_course(*, instructor: BaseUser, title: str, category: str , is_public:bool):
     

     course =Course.objects.create(
        instructor=instructor, title=title, category=category, slug=slugify(title), is_public=is_public
    )
     return course


def delete_course(*, user: BaseUser, slug: str) :
    course = Course.objects.get(slug=slug).delete()
    return course
 
