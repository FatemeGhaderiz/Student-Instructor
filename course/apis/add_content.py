from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.validators import ValidationError

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Content,Course,Exercise, Announcement
from ..services.add_content import create_content , create_exercise , create_announcement
from ..permissions import IsContentCreatorOrReadOnly


class AddContentApi(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [MultiPartParser]
    

    class InputContentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        file = serializers.FileField(required=False)
        text = serializers.CharField(required=False)

        def validate(self, data):
            request = self.context.get('request')
            slug = self.context.get('slug')
            
            course = Course.objects.get(slug=slug)
            if request.user != course.instructor:
                raise ValidationError({"messege":"you are not instructor"})
            return data
            

    class OutPutContentSerializer(serializers.ModelSerializer):
        course = serializers.SerializerMethodField("get_course")

        class Meta:
            model = Content
            fields = ("course","title", "file", "text")

        def get_course(self, content):
            
            return content.course.title

    @extend_schema(
        responses=InputContentSerializer,
        request=OutPutContentSerializer,
    )
    def post(self, request , slug):
        serializer = self.InputContentSerializer(data=request.data , context = {'request':request , 'slug' : slug})
        serializer.is_valid(raise_exception=True)
        try:
            query = create_content(
                course=slug,
                title=serializer.validated_data.get("title"),
                file=serializer.validated_data.get("file"),
                text=serializer.validated_data.get("text"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutContentSerializer(query, context={"request":request}).data)


# Exercise


class AddExerciseApi(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [MultiPartParser]
    

    class InputExerciseSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        file = serializers.FileField(required=False)
        text = serializers.CharField(required=False)
        deadline = serializers.DateField()

        def validate(self, data):
            request = self.context.get('request')
            slug = self.context.get('slug')
            
            course = Course.objects.get(slug=slug)
            if not(request.user == course.instructor):
                raise ValidationError({"messege":"you are not instructor"})
            return data
            

    class OutPutExerciseSerializer(serializers.ModelSerializer):
        course = serializers.SerializerMethodField("get_course")

        class Meta:
            model = Exercise
            fields = ("course","title", "file", "text","deadline")

        def get_course(self, exercise):
            
            return exercise.course.title

    @extend_schema(
        responses=InputExerciseSerializer,
        request=OutPutExerciseSerializer,
    )
    def post(self, request , slug):
        serializer = self.InputExerciseSerializer(data=request.data , context = {'request':request , 'slug' : slug})
        serializer.is_valid(raise_exception=True)
        try:
            query = create_exercise(
                course=slug,
                title=serializer.validated_data.get("title"),
                file=serializer.validated_data.get("file"),
                text=serializer.validated_data.get("text"),
                deadline=serializer.validated_data.get("deadline"),

            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutExerciseSerializer(query, context={"request":request}).data)

 

# Announcement

class AddAnnouncementApi(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [MultiPartParser]
    

    class InputAnnouncementSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        text = serializers.CharField()

        def validate(self, data):
            request = self.context.get('request')
            slug = self.context.get('slug')
            
            course = Course.objects.get(slug=slug)
            if request.user != course.instructor:
                raise ValidationError({"messege":"you are not instructor"})
            return data
            

    class OutPutAnnouncementSerializer(serializers.ModelSerializer):
        course = serializers.SerializerMethodField("get_course")

        class Meta:
            model = Content
            fields = ("course","title", "text")

        def get_course(self, content):
            
            return content.course.title

    @extend_schema(
        responses=InputAnnouncementSerializer,
        request=OutPutAnnouncementSerializer,
    )
    def post(self, request , slug):
        serializer = self.InputAnnouncementSerializer(data=request.data , context = {'request':request , 'slug' : slug})
        serializer.is_valid(raise_exception=True)
        try:
            query = create_announcement(
                course=slug,
                title=serializer.validated_data.get("title"),
                text=serializer.validated_data.get("text"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutAnnouncementSerializer(query, context={"request":request}).data)
