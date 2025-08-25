from rest_framework import viewsets, permissions, decorators, response, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models
from .models import Course
from .serializers import CourseSerializer, CourseWriteSerializer, UserBriefSerializer
from .permissions import IsCourseTeacher

User = get_user_model()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy','add_student','remove_student','add_teacher']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CourseWriteSerializer
        return CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Course.objects.none()
        if user.is_staff or (hasattr(user, 'is_teacher') and user.is_teacher()):
            return Course.objects.filter(models.Q(owner=user)|models.Q(teachers=user)).distinct()
        return Course.objects.filter(students=user)

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.teachers.add(self.request.user)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def check_object_permissions(self, request, obj):
        if request.method in ('GET','HEAD','OPTIONS'):
            return
        if not IsCourseTeacher().has_object_permission(request, self, obj):
            self.permission_denied(request, message="Not a course teacher.")
        
    @decorators.action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        student = get_object_or_404(User, id=student_id, role='student')
        if not (course.owner_id == request.user.id or course.teachers.filter(id=request.user.id).exists()):
            return response.Response({'detail':'Only teachers can add students.'}, status=status.HTTP_403_FORBIDDEN)
        course.students.add(student)
        return response.Response({'status':'student added', 'student': UserBriefSerializer(student).data})

    @decorators.action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        student = get_object_or_404(User, id=student_id, role='student')
        if not (course.owner_id == request.user.id or course.teachers.filter(id=request.user.id).exists()):
            return response.Response({'detail':'Only teachers can remove students.'}, status=status.HTTP_403_FORBIDDEN)
        course.students.remove(student)
        return response.Response({'status':'student removed', 'student_id': student.id})

    @decorators.action(detail=True, methods=['post'])
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        teacher = get_object_or_404(User, id=teacher_id, role='teacher')
        if course.owner_id != request.user.id:
            return response.Response({'detail':'Only owner can add teachers.'}, status=status.HTTP_403_FORBIDDEN)
        course.teachers.add(teacher)
        return response.Response({'status':'teacher added', 'teacher': UserBriefSerializer(teacher).data})
