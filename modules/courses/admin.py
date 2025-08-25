from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
