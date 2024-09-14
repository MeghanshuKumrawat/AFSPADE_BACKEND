from rest_framework import viewsets
from main.models import Course, Assignment, Question
from main.serializers import CourseReadSerializer, CourseWriteSerializer, AssignmentReadSerializer, AssignmentWriteSerializer, QuestionReadSerializer, QuestionWriteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseWriteSerializer
        return CourseReadSerializer

    def perform_create(self, serializer):
        # Check if the user is a teacher
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can create courses.")
        # Set the current user as the teacher for the course
        serializer.save(teacher=self.request.user)

    def perform_update(self, serializer):
        # Check if the current user is the teacher for the course
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can update courses.")
        if serializer.instance.teacher != self.request.user:
            raise PermissionDenied("You can only update courses you created.")
        serializer.save()

    def get_queryset(self):
        # Filter to only return courses taught by the current teacher
        if self.request.user.is_teacher:
            return Course.objects.filter(teacher=self.request.user)
        return Course.objects.none()  # Non-teachers cannot access courses

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AssignmentWriteSerializer
        return AssignmentReadSerializer

    def perform_create(self, serializer):
        # Check if the user is a teacher
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can create assignments.")
        
        # Get the course instance from the request data
        course_id = self.request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Check if the current user is the teacher of the course
        if course.teacher != self.request.user:
            raise PermissionDenied("You can only create assignments for courses you teach.")
        
        # Save the assignment with the course and teacher
        serializer.save(course=course)

    def perform_update(self, serializer):
        # Check if the user is a teacher
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can update assignments.")
        
        # Check if the current user is the teacher for the course
        if serializer.instance.course.teacher != self.request.user:
            raise PermissionDenied("You can only update assignments for courses you teach.")
        
        # Save the assignment
        serializer.save()

    def get_queryset(self):
        # Filter to only return assignments for courses taught by the current teacher
        queryset = Assignment.objects.filter(course__teacher=self.request.user)
        
        # Check for course_id in the query parameters
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        return queryset
    
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionWriteSerializer
        return QuestionReadSerializer

    def perform_create(self, serializer):
        # Check if the user is a teacher
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can create questions.")
        
        # Get the assignment instance from the request data
        assignment_id = self.request.data.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)

        # Check if the current user is the teacher of the course related to the assignment
        if assignment.course.teacher != self.request.user:
            raise PermissionDenied("You can only create questions for assignments in courses you teach.")
        
        # Save the question with the assignment
        serializer.save(assignment=assignment)

    def perform_update(self, serializer):
        # Check if the user is a teacher
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can update questions.")
        
        # Check if the current user is the teacher for the course related to the assignment
        if serializer.instance.assignment.course.teacher != self.request.user:
            raise PermissionDenied("You can only update questions for assignments in courses you teach.")
        
        # Save the question
        serializer.save()

    def get_queryset(self):
        # Filter to only return questions for assignments in courses taught by the current teacher
        queryset = Question.objects.filter(assignment__course__teacher=self.request.user)
        
        # Check for assignment_id in the query parameters
        assignment_id = self.request.query_params.get('assignment_id')
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)
        
        return queryset