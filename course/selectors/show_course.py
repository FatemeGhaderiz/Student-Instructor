from users.models import BaseUser

from ..models import CourseEnrollment , Course
from rest_framework.validators import ValidationError
def course_list(*, user:BaseUser ) :
   
   
    queryset = CourseEnrollment.objects.filter(student=user)

    return queryset
   

def course_detail(*, slug:str , user:BaseUser):
    course = Course.objects.get(slug=slug)
    enrollment = CourseEnrollment.objects.get(course=course , student=user)
    if   enrollment == None  :
        return None
    return course
         
         
    

    