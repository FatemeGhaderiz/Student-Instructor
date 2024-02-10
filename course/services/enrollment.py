

from ..models import Course , CourseEnrollment
from users.models import BaseUser
import datetime




def create_enrollment(*, user: BaseUser, course: str):
     

     content =CourseEnrollment.objects.create(
        student = user,
        course=Course.objects.get(title=course)
    )
     return content

