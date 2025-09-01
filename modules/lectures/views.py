from rest_framework import viewsets, permissions, decorators, response, status
from . import services
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from modules.courses.models import Course
from .models import Lecture, HomeworkAssignment, Submission, Grade, GradeComment
from .serializers import (
    LectureSerializer, HomeworkAssignmentSerializer,
    SubmissionSerializer, GradeSerializer, GradeCommentSerializer
)

User = get_user_model()

class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all().select_related('course').order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Lecture.objects.none()
        return Lecture.objects.filter(
            Q(course__owner=user) | Q(course__teachers=user) | Q(course__students=user)
        ).distinct()

class HomeworkAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = HomeworkAssignmentSerializer
    queryset = HomeworkAssignment.objects.all().select_related('lecture','lecture__course').order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return HomeworkAssignment.objects.none()
        return HomeworkAssignment.objects.filter(
            Q(lecture__course__owner=user) | Q(lecture__course__teachers=user) | Q(lecture__course__students=user)
        ).distinct()

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all().select_related('lecture','lecture__course','student').order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Submission.objects.none()
        if hasattr(user, 'is_teacher') and user.is_teacher():
            return Submission.objects.filter(
                Q(lecture__course__owner=user) | Q(lecture__course__teachers=user)
            ).distinct()
        return Submission.objects.filter(student=user)

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all().select_related('submission','submission__lecture','submission__lecture__course').order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Grade.objects.none()
        if hasattr(user,'is_teacher') and user.is_teacher():
            return Grade.objects.filter(
                Q(submission__lecture__course__owner=user) | Q(submission__lecture__course__teachers=user)
            )
        return Grade.objects.filter(submission__student=user)

class GradeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = GradeCommentSerializer
    queryset = GradeComment.objects.all().select_related('grade','author','grade__submission').order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return GradeComment.objects.none()
        return GradeComment.objects.filter(
            Q(grade__submission__lecture__course__owner=user) |
            Q(grade__submission__lecture__course__teachers=user) |
            Q(grade__submission__student=user) |
            Q(author=user)
        ).distinct()
