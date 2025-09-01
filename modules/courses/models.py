from django.db import models
from django.conf import settings


class CourseQuerySet(models.QuerySet):
    def is_available(self):
        try:
            return self.filter(is_active=True)
        except Exception:
            return self

    def with_teacher(self, user=None):
        try:
            return self.filter(teachers__in=[user]) if user else self
        except Exception:
            return self

    def for_teacher(self, user):
        try:
            return self.filter(teacher=user) | self.filter(teachers__in=[user])
        except Exception:
            return self.filter(teacher=user)

class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def is_available(self):
        return self.get_queryset().is_available()

    def with_teacher(self, user=None):
        return self.get_queryset().with_teacher(user=user)

    def for_teacher(self, user):
        return self.get_queryset().for_teacher(user)

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    objects = CourseManager()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_courses')
    teachers = models.ManyToManyField(User, related_name='teaching_courses', blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
