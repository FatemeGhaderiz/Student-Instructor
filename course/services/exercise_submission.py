from ..models import Course, Content, Exercise, Announcement, ExerciseSubmission
from users.models import BaseUser
import datetime

from django.utils.text import slugify


def create_exercise_submission(
    *, student: BaseUser, exercise: str, file: str, text: str
):

    exercise = ExerciseSubmission.objects.create(
        student=student,
        exercise=Exercise.objects.get(slug=exercise),
        file=file,
        text=text,
    )
    return exercise
