from django.urls import path
from .apis.add_course import  AddCourseApi
from .apis.add_content import AddContentApi, AddExerciseApi, AddAnnouncementApi


urlpatterns = [
    path('add-course/', AddCourseApi.as_view(),name="add-course"),
    path('add-content/<slug:slug>', AddContentApi.as_view(),name="add-content"),
    path('add-exercise/<slug:slug>', AddExerciseApi.as_view(),name="add-exercise"),
    path('add-announcement/<slug:slug>', AddAnnouncementApi.as_view(),name="add-announcement"),
]
