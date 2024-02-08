from django.urls import path
from .apis.add_course import  AddCourseApi


urlpatterns = [
    path('add-course/', AddCourseApi.as_view(),name="add-course"),
]
