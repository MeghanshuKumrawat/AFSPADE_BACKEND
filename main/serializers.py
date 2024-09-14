from rest_framework import serializers
from .models import Course, Assignment, Question

class CourseReadSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'level', 'semester', 'thumbnail', 'teacher_name']

class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'level', 'semester', 'thumbnail']
        # The 'teacher' field should not be required in the input as it will be set automatically
        extra_kwargs = {
            'teacher': {'read_only': True}
        }
class QuestionReadSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'assignment', 'assignment_title', 'text', 'language']

class QuestionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['assignment', 'text', 'language']

        extra_kwargs = {
            'assignment': {'read_only': True}
        }

class AssignmentReadSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    questions = QuestionReadSerializer(many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'course', 'course_name', 'title', 'description', 'deadline', 'created_at', 'questions']

class AssignmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'deadline']

        extra_kwargs = {
            'course': {'read_only': True}
        }
