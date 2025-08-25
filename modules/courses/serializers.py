from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','role')

class CourseSerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only=True)
    teachers = UserBriefSerializer(many=True, read_only=True)
    students = UserBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id','title','description','owner','teachers','students','created_at')

class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title','description')
