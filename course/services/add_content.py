from ..models import Course , Content
from users.models import BaseUser

from django.db import transaction
from django.utils.text import slugify



def create_content(*, course: str, title: str, file: str , text:str):
     

     content =Content.objects.create(
        course=Course.objects.get(slug=course), title=title, file=file, text=text
    )
     return content