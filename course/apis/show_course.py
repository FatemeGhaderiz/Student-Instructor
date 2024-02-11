from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse

from drf_spectacular.utils import extend_schema

from api.pagination import  get_paginated_response, LimitOffsetPagination, get_paginated_response_context
from rest_framework.pagination import PageNumberPagination

from ..models import CourseEnrollment,Course,Content,Exercise,Announcement

from ..selectors.show_course import course_list,course_detail

from ..serializers import OutPutAnnouncementSerializer, OutPutExerciseSerializer,OutPutContentSerializer


class CourseListApi(APIView):

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutPutCourseSerializer(serializers.ModelSerializer):
        instructor = serializers.SerializerMethodField("get_instructor")
        course = serializers.SerializerMethodField("get_course")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = CourseEnrollment
            fields = ("course", "instructor", "url" )

        def get_instructor(self, enrollment):
            return enrollment.course.instructor.email
        
        def get_course(self, enrollment):
            return enrollment.course.title
        
        def get_url(self, enrollment):
            request = self.context.get("request")
            path = reverse("api:course:course-detail", args=(enrollment.course.slug,))
            return request.build_absolute_uri(path)



    @extend_schema(
        responses=OutPutCourseSerializer,
    )
    def get(self , request):
        query = course_list(user=request.user)
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutCourseSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class CourseDetailApi(APIView):
    permission_classes = [IsAuthenticated]



    class OutPutDetailSerializer(serializers.ModelSerializer):
        exercises = OutPutExerciseSerializer(many=True, read_only=True)
        contents = OutPutContentSerializer(many=True, read_only=True)
        announcements = OutPutAnnouncementSerializer(many=True, read_only=True)
        instructor = serializers.SerializerMethodField("get_instructor")

        class Meta:
            model = Course
            fields = ("title", "category", "is_public" ,"instructor" ,"contents" , "exercises" , "announcements")

        def get_instructor(self, course):
            return course.instructor.email


    @extend_schema(
        responses=OutPutDetailSerializer,
    )
    def get(self, request, slug):

        try:
            query = course_detail(slug=slug, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.OutPutDetailSerializer(query)

        return Response(serializer.data) 
