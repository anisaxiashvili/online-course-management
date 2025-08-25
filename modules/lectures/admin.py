from django.contrib import admin
from .models import Lecture, HomeworkAssignment, Submission, Grade, GradeComment

admin.site.register(Lecture)
admin.site.register(HomeworkAssignment)
admin.site.register(Submission)
admin.site.register(Grade)
admin.site.register(GradeComment)
