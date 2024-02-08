from django.urls import path, include

urlpatterns = [
    path('users/', include(('users.urls', 'users'))),
    path('auth/', include(('authentication.urls', 'auth'))),
     path('course/', include(('course.urls', 'course'))),
 ]
