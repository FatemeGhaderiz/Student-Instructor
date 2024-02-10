

from ..models import Course , CourseEnrollment
from users.models import BaseUser
import datetime




def create_enrollment(*, user: BaseUser, course: str):
     

     content =CourseEnrollment.objects.create(
        student = user,
        course=Course.objects.get(title=course)
    )
     return content

def create_private_enrollment(*, user: str, slug: str):
     
     student = BaseUser.objects.get(email = user)
     course=Course.objects.get(slug=slug)
     content =CourseEnrollment.objects.create(
        student = student,
        course = course
    )
     return content