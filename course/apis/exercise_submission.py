from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.validators import ValidationError

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from ..models import Content, Course, Exercise, ExerciseSubmission, CourseEnrollment
from ..services.exercise_submission import create_exercise_submission
from users.models import BaseUser
from ..permissions import IsContentCreatorOrReadOnly
from datetime import date


class ExerciseSubmissionApi(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    class InputExerciseSubmissionSerializer(serializers.Serializer):
        file = serializers.FileField(required=False)
        text = serializers.CharField(required=False)

        def validate(self, data):
            request = self.context.get("request")
            slug = self.context.get("slug")
            exercise = Exercise.objects.get(slug=slug)
            if date.today() >= exercise.deadline:
                raise ValidationError({"messege": "time out"})
            return data

    class OutPutExerciseSubmissionSerializer(serializers.ModelSerializer):
        student = serializers.SerializerMethodField("get_student")

        class Meta:
            model = ExerciseSubmission
            fields = ("student", "exercise", "file", "text")

        def get_student(self, exercise_submission):

            return exercise_submission.student.email

    @extend_schema(
        responses=OutPutExerciseSubmissionSerializer,
        request=InputExerciseSubmissionSerializer,
    )
    def post(self, request, slug):
        serializer = self.InputExerciseSubmissionSerializer(
            data=request.data, context={"request": request, "slug": slug}
        )
        serializer.is_valid(raise_exception=True)
        try:
            query = create_exercise_submission(
                exercise=slug,
                student=request.user,
                file=serializer.validated_data.get("file"),
                text=serializer.validated_data.get("text"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            self.OutPutExerciseSubmissionSerializer(
                query, context={"request": request}
            ).data
        )
