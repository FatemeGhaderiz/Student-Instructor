from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Course
from ..services.add_course import create_course 



class AddCourseApi(APIView):
   
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        category = serializers.CharField(max_length=255)
        is_public = serializers.BooleanField()

    class OutPutSerializer(serializers.ModelSerializer):
        instructor = serializers.SerializerMethodField("get_instructor")

        class Meta:
            model = Course
            fields = ("slug","title", "category", "is_public" ,"instructor")

        def get_instructor(self, course):
            return course.instructor.email


    @extend_schema(
        responses=OutPutSerializer,
        request=InputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = create_course(
                instructor=request.user,
                title=serializer.validated_data.get("title"),
                category=serializer.validated_data.get("category"),
                is_public=serializer.validated_data.get("is_public"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializer(query, context={"request":request}).data)

 