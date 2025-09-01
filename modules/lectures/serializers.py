from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Lecture, HomeworkAssignment, Submission, Grade, GradeComment

User = get_user_model()

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id','course','topic','presentation','created_at')
        read_only_fields = ('id','created_at')

class HomeworkAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAssignment
        fields = ('id','lecture','title','description','due_at','created_at')
        read_only_fields = ('id','created_at')

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id','assignment','student','text','attachment','created_at')
        read_only_fields = ('id','student','created_at')

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id','submission','grader','score','feedback','created_at')
        read_only_fields = ('id','grader','created_at')

    def validate_score(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError('Score must be between 0 and 100.')
        return value

class GradeCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GradeComment
        fields = ('id','grade','author','text','created_at')
        read_only_fields = ('id','author','created_at')