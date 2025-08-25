from rest_framework import serializers
from django.contrib.auth import get_user_model
from modules.courses.models import Course
from .models import Lecture, HomeworkAssignment, Submission, Grade, GradeComment

User = get_user_model()

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id','course','topic','presentation','created_at')
        read_only_fields = ('id','created_at')

    def validate(self, attrs):
        request = self.context['request']
        course = attrs.get('course') or getattr(self.instance, 'course', None)
        if request.method in ('POST','PUT','PATCH') and course:
            if not (course.owner_id == request.user.id or course.teachers.filter(id=request.user.id).exists()):
                raise serializers.ValidationError('Only course teachers can create/update lectures.')
        return attrs

class HomeworkAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAssignment
        fields = ('id','lecture','text','created_at')
        read_only_fields = ('id','created_at')

    def validate(self, attrs):
        request = self.context['request']
        lecture = attrs.get('lecture') or getattr(self.instance, 'lecture', None)
        if request.method in ('POST','PUT','PATCH') and lecture:
            course = lecture.course
            if not (course.owner_id == request.user.id or course.teachers.filter(id=request.user.id).exists()):
                raise serializers.ValidationError('Only course teachers can manage assignments.')
        return attrs

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id','lecture','student','text','file','created_at')
        read_only_fields = ('id','student','created_at')

    def validate(self, attrs):
        request = self.context['request']
        lecture = attrs.get('lecture') or getattr(self.instance, 'lecture', None)
        if lecture:
            course = lecture.course
            if not course.students.filter(id=request.user.id).exists():
                raise serializers.ValidationError('You must be enrolled in the course to submit.')
        return attrs

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id','submission','grader','score','feedback','updated_at')
        read_only_fields = ('id','grader','updated_at')

    def validate_score(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError('Score must be between 0 and 100.')
        return value

    def validate(self, attrs):
        request = self.context['request']
        submission = attrs.get('submission') or getattr(self.instance, 'submission', None)
        if submission:
            course = submission.lecture.course
            if not (course.owner_id == request.user.id or course.teachers.filter(id=request.user.id).exists()):
                raise serializers.ValidationError('Only course teachers can grade.')
        return attrs

    def create(self, validated_data):
        validated_data['grader'] = self.context['request'].user
        return super().create(validated_data)

class GradeCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GradeComment
        fields = ('id','grade','author','text','created_at')
        read_only_fields = ('id','author','created_at')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
