from django.urls import path
from .apis.add_course import  AddCourseApi
from .apis.add_content import AddContentApi


urlpatterns = [
    path('add-course/', AddCourseApi.as_view(),name="add-course"),
    path('add-content/<slug:slug>', AddContentApi.as_view(),name="add-content"),
]
