from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCourseTeacher(BasePermission):
    """Teachers of a course (owner or in teachers) can modify it."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        return (obj.owner_id == user.id) or obj.teachers.filter(id=user.id).exists()
