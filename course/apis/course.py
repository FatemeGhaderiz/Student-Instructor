from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Course
from ..services.course import create_course, delete_course

from ..permissions import IsContentCreatorOrReadOnly


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
            fields = ("slug", "title", "category", "is_public", "instructor")

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
        return Response(self.OutPutSerializer(query, context={"request": request}).data)














class UpdateAndDeleteCourseApi(APIView):

    permission_classes = [IsAuthenticated, IsContentCreatorOrReadOnly]

    class UpdaeSerializer(serializers.ModelSerializer):
        instructor = serializers.SerializerMethodField("get_instructor", read_only=True)

        class Meta:
            model = Course
            fields = ("title", "category", "is_public", "instructor")

        def get_instructor(self, course):
            return course.instructor.email

    @extend_schema(
        responses=UpdaeSerializer,
        request=UpdaeSerializer,
    )
    def put(self, request, slug):
        instance = Course.objects.get(slug=slug)
        self.check_object_permissions(request, instance)
        serializer = self.UpdaeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                query = serializer.update(
                    instance=instance, validated_data=serializer.validated_data
                )
            except Exception as ex:

                return Response(
                    {"detail": "Database Error - " + str(ex)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                self.UpdaeSerializer(query, context={"request": request}).data
            )

    def delete(self, request, slug):

        try:
            instance = Course.objects.get(slug=slug)
            self.check_object_permissions(request, instance)
            instance.delete()
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"messege": " deleted"}, status=status.HTTP_204_NO_CONTENT)


# class UDCourseViwe(APIView):
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticated , IsUser]


#     class InputSerializer(serializers.Serializer):
#         title = serializers.CharField(max_length=255)
#         category = serializers.CharField(max_length=255)
#         is_public = serializers.BooleanField()

#     class OutPutSerializer(serializers.ModelSerializer):
#         instructor = serializers.SerializerMethodField("get_instructor")

#         class Meta:
#             model = Course
#             fields = ("title", "category", "is_public" ,"instructor")

#         def get_instructor(self, course):
#             return course.instructor.email


#     def put(self , request, pk=None):
#         instance = Course.objects.get(id=pk)
#         self.check_object_permissions(request,instance)
#         serializer = self.InputSerializer(data=request.data , partial = True)
#         if serializer.is_valid():
#             serializer.update(instance=instance, validated_data=serializer.validated_data)
#             return Response({"messege" : " update"})


#     def delete(self , request, pk=None):
#         instance = Course.objects.get(id=pk)
#         self.check_object_permissions(request,instance)
#         instance.delete()
#         return Response({"messege" : " deleted"})
