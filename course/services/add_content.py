from ..models import Course , Content, Exercise ,Announcement
from users.models import BaseUser
import datetime




def create_content(*, course: str, title: str, file: str , text:str):
     

     content =Content.objects.create(
        course=Course.objects.get(slug=course), title=title, file=file, text=text
    )
     return content



def create_exercise(*, course: str, title: str, file: str , text:str , deadline : datetime.date):
     

     exercise =Exercise.objects.create(
        course=Course.objects.get(slug=course), title=title, file=file, text=text, deadline=deadline
    )
     return exercise


def create_announcement(*, course: str, title: str , text:str ):
     

     announcement =Announcement.objects.create(
        course=Course.objects.get(slug=course), title=title, text=text
    )
     return announcement