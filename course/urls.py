from django.urls import path
from .apis.add_course import  AddCourseApi
from .apis.add_content import AddContentApi, AddExerciseApi, AddAnnouncementApi
from .apis.enrollment import EnrollmentApi,PrivateEnrollmentApi
from .apis.show_course import CourseListApi, CourseDetailApi


urlpatterns = [
    path('add-course/', AddCourseApi.as_view(),name="add-course"),
    path('add-content/<slug:slug>', AddContentApi.as_view(),name="add-content"),
    path('add-exercise/<slug:slug>', AddExerciseApi.as_view(),name="add-exercise"),
    path('add-announcement/<slug:slug>', AddAnnouncementApi.as_view(),name="add-announcement"),
    path('enrollment', EnrollmentApi.as_view(),name="enrollment"),
    path('enrollment-private/<slug:slug>', PrivateEnrollmentApi.as_view(),name="enrollment-private"),
    path('course-list', CourseListApi.as_view(),name="course-list"),
    path('course-detail/<slug:slug>', CourseDetailApi.as_view(),name="course-detail"),
]
