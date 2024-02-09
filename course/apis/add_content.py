from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Content
from ..services.add_content import create_content 
from ..permissions import IsUser


class AddContentApi(APIView):
    permission_classes = [IsAuthenticated , IsUser]
    parser_classes = [MultiPartParser]

    class InputContentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        file = serializers.FileField(required=False)
        text = serializers.CharField(required=False)

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
        serializer = self.InputContentSerializer(data=request.data)
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

 