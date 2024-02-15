from django.urls import reverse
import pytest

from course.services.course import create_course
from users.models import BaseUser



@pytest.fixture
def common_user():
    user = BaseUser.objects.create_user(
        email="admin@admin.com", password="a/@1234567", username = "admin"
    )
    return user





@pytest.mark.django_db
def test_create_course(common_user):
    a = create_course(instructor = common_user, title="test", category="category" ,is_public = True)

    assert a.instructor == common_user
    assert a.title == "test"
    assert a.category == "category"
    assert a.is_public == True
