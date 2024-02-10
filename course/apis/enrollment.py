from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.validators import ValidationError

from drf_spectacular.utils import extend_schema


from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Course,CourseEnrollment
from ..services.enrollment import create_enrollment 



class EnrollmentApi(APIView):
    permission_classes = [ IsAuthenticated ]
    

    class InputEnrollmentSerializer(serializers.Serializer):

        course = serializers.CharField(max_length=255)
       

        def validate(self, data):
            request = self.context.get('request')
            course = Course.objects.get(title = data["course"])

            if course.is_public == False:
                raise ValidationError({"messege":"Course is not publish"})
            
            if request.user == course.instructor:
                 raise ValidationError({"messege":"You are instructor"})
            return data
        

        
            

    class OutPutEnrollmentSerializer(serializers.ModelSerializer):
        course = serializers.SerializerMethodField("get_course")
        student = serializers.SerializerMethodField("get_student")

        class Meta:
            model = CourseEnrollment
            fields = ("course","student")

        def get_course(self, enrollment):
            return enrollment.course.title

        
        def get_student(self, enrollment):
            request = self.context.get('request')
            return request.user.email

    @extend_schema(
        responses=OutPutEnrollmentSerializer,
        request=InputEnrollmentSerializer,
    )
    def post(self, request ):
        serializer = self.InputEnrollmentSerializer(data=request.data , context = {'request':request })
        serializer.is_valid(raise_exception=True)
        try:
            query = create_enrollment(
                 user=request.user,
                 course=serializer.validated_data.get("course"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutEnrollmentSerializer(query, context={"request":request}).data)

