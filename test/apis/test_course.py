from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from users.models import BaseUser



@pytest.fixture
def common_user():
    user = BaseUser.objects.create_user(
        email="admin@admin.com", password="a/@1234567", username = "admin"
    )
    return user


@pytest.mark.django_db
class TestPostApi:

    client = APIClient()

    def test_get_course_list_response_401_status(self):
        url = reverse("api:course:course-list")
        response = self.client.get(url)
        assert response.status_code == 401

    
    def test_create_course_response_401_status(self,common_user):
        url = reverse("api:course:add-course")
        data = {
            "title": "test",
            "category": "test",
            "is_public": True,
        }
        response = self.client.post(url, data)
        assert response.status_code == 401


    def test_get_course_list_response_200_status(self,common_user):
        url = reverse("api:course:course-list")
        self.client.force_authenticate(user=common_user)
        response = self.client.get(url)
        assert response.status_code == 200    


    def test_create_course_invalid_data_response_400_status(
        self, common_user):
        url = reverse("api:course:add-course")
        data = {"title": "test",}
        user = common_user

        self.client.force_authenticate(user=common_user)
        response = self.client.post(url, data)
        assert response.status_code == 400


    def test_create_course_response_200_status(self,common_user):
        url = reverse("api:course:add-course")
        data = {
            "title": "test",
            "category": "test",
            "is_public": True,
        }
        self.client.force_authenticate(user=common_user)
        response = self.client.post(url, data)
        assert response.status_code == 200

   


