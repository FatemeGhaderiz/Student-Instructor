from django.urls import path
from .apis.add_course import  AddCourseApi
from .apis.add_content import AddContentApi, AddExerciseApi, AddAnnouncementApi
from .apis.enrollment import EnrollmentApi,PrivateEnrollmentApi


urlpatterns = [
    path('add-course/', AddCourseApi.as_view(),name="add-course"),
    path('add-content/<slug:slug>', AddContentApi.as_view(),name="add-content"),
    path('add-exercise/<slug:slug>', AddExerciseApi.as_view(),name="add-exercise"),
    path('add-announcement/<slug:slug>', AddAnnouncementApi.as_view(),name="add-announcement"),
    path('enrollment', EnrollmentApi.as_view(),name="enrollment"),
    path('enrollment-private/<slug:slug>', PrivateEnrollmentApi.as_view(),name="enrollment-private"),
]
