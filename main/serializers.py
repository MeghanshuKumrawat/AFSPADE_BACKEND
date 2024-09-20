from rest_framework import serializers
from .models import Course, Assignment, Question, CourseEnrollment, Submission

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

class CourseEnrollmentReadSerializer(serializers.ModelSerializer):
    course = CourseReadSerializer(read_only=True)  # Nested serializer for course details
    student_name = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'student_name', 'enrolled_at']

class CourseEnrollmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ['course', 'student', 'enrolled_at']
        read_only_fields = ['student', 'enrolled_at', 'course']

class SubmissionReadSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'question_text', 'code_text', 'submitted_at', 'is_graded', 'is_final', 'grade', 'feedback']

class SubmissionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['question', 'code_text']  # Exclude 'student', will be set in the view
        read_only_fields = ['submitted_at', 'is_graded', 'is_final', 'grade', 'feedback']

class AssignmentWithSubmissionsSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    submissions = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'deadline', 'created_at', 'course_name', 'course_code', 'submissions']

    def get_submissions(self, obj):
        # Get all submissions related to the assignment via the question relationship
        submissions = Submission.objects.filter(question__assignment=obj)
        return SubmissionReadSerializer(submissions, many=True).data

