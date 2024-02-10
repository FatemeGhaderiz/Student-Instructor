from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsContentCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        # Allow GET, HEAD, or OPTIONS requests
        if request.method in SAFE_METHODS:
            print('no')
            return True

        # Check if the user creating the content is the same user who created the course
        print ("yes")
        return obj.course.instructor == request.user