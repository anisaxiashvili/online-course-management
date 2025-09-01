from django.db import transaction
from django.core.exceptions import ValidationError

@transaction.atomic
def add_student_to_course(course, student):
    if hasattr(course, 'students') and course.students.filter(pk=student.pk).exists():
        raise ValidationError("Student already enrolled.")
    if hasattr(course, 'students'):
        course.students.add(student)
    return course

@transaction.atomic
def add_teacher_to_course(course, teacher):
    if hasattr(course, 'teachers') and course.teachers.filter(pk=teacher.pk).exists():
        raise ValidationError("Teacher already assigned.")
    if hasattr(course, 'teachers'):
        course.teachers.add(teacher)
    elif hasattr(course, 'teacher'):
        course.teacher = teacher
        course.save(update_fields=['teacher'])
    return course