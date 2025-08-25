from django.db import models
from django.conf import settings
from modules.courses.models import Course

User = settings.AUTH_USER_MODEL

def presentation_upload_path(instance, filename):
    return f'presentations/course_{instance.course_id}/{filename}'

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    topic = models.CharField(max_length=255)
    presentation = models.FileField(upload_to=presentation_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.title} :: {self.topic}'

class HomeworkAssignment(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name='assignment')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecture', 'student')

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    grader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades_given')
    score = models.PositiveSmallIntegerField()
    feedback = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class GradeComment(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
