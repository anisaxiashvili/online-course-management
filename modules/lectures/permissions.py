from rest_framework.permissions import BasePermission, SAFE_METHODS
from modules.courses.models import Course

class IsCourseTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        course = obj.course if hasattr(obj, 'course') else getattr(getattr(obj,'lecture',None),'course', None)
        if not course:
            return False
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        return (course.owner_id == user.id) or course.teachers.filter(id=user.id).exists()

class IsEnrolledStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        course = obj.course if hasattr(obj, 'course') else getattr(getattr(obj,'lecture',None),'course', None)
        if not course:
            return False
        if request.method in SAFE_METHODS:
            return True
        return course.students.filter(id=request.user.id).exists()
