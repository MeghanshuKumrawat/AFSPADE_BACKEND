from rest_framework import viewsets
from rest_framework.views import APIView
from accounts.models import User
from main.models import Course, Assignment, CourseEnrollment, Submission
from main.serializers import (CourseReadSerializer, CourseWriteSerializer, AssignmentReadSerializer, AssignmentWriteSerializer, CourseEnrollmentWriteSerializer, CourseEnrollmentReadSerializer, SubmissionReadSerializer, SubmissionWriteSerializer, AssignmentWithSubmissionsSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.utils import timezone

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
        # Get the 'active' filter from query parameters
        is_active = self.request.query_params.get('active', None)

        # Filter for teachers (show only their own courses)
        if self.request.user.is_teacher:
            queryset = Course.objects.filter(teacher=self.request.user)

        # Filter for students (show only courses matching their level and semester)
        elif self.request.user.is_student:
            queryset = Course.objects.filter(level=self.request.user.level, semester=self.request.user.semester)
            # If a search query is provided, filter the results further
            if self.request.query_params.get("search"):
                query = self.request.query_params.get("search")
                queryset = queryset.filter(Q(name__icontains=query) | Q(code__contains=query))

        else:
            queryset = Course.objects.none()

        # Apply the 'active' filter if provided
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset.distinct()

    def get_queryset(self):
        # Filter to only return courses taught by the current teacher
        if self.request.user.is_teacher:
            return Course.objects.filter(teacher=self.request.user)
        if self.request.user.is_student:
            # return Course.objects.all()
            if self.request.query_params.get("search"):
                query = self.request.query_params.get("search")
                return Course.objects.filter(level=self.request.user.level, semester=self.request.user.semester).filter(Q(name__icontains=query) | Q(code__contains=query)).distinct()
            return Course.objects.filter(level=self.request.user.level, semester=self.request.user.semester)
        return Course.objects.none()  

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
        
        if self.request.user.is_teacher:
            queryset = Assignment.objects.filter(course__teacher=self.request.user)
        if self.request.user.is_student:
            queryset = Assignment.objects.filter(course__enrollments__student=self.request.user)

        # Check for course_id in the query parameters
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        
        return queryset
    
# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
#     pagination_class = PageNumberPagination

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return QuestionWriteSerializer
#         return QuestionReadSerializer

#     def perform_create(self, serializer):
#         # Check if the user is a teacher
#         if not self.request.user.is_teacher:
#             raise PermissionDenied("Only teachers can create questions.")
        
#         # Get the assignment instance from the request data
#         assignment_id = self.request.data.get('assignment_id')
#         assignment = get_object_or_404(Assignment, id=assignment_id)

#         # Check if the current user is the teacher of the course related to the assignment
#         if assignment.course.teacher != self.request.user:
#             raise PermissionDenied("You can only create questions for assignments in courses you teach.")
        
#         # Save the question with the assignment
#         serializer.save(assignment=assignment)

#     def perform_update(self, serializer):
#         # Check if the user is a teacher
#         if not self.request.user.is_teacher:
#             raise PermissionDenied("Only teachers can update questions.")
        
#         # Check if the current user is the teacher for the course related to the assignment
#         if serializer.instance.assignment.course.teacher != self.request.user:
#             raise PermissionDenied("You can only update questions for assignments in courses you teach.")
        
#         # Save the question
#         serializer.save()

#     def get_queryset(self):
#         queryset = Question.objects.none()  # Start with an empty queryset as a default
#         print(self.request.user.is_student , '------------')

#         if self.request.user.is_teacher:
#             # Teachers can see all questions for assignments in courses they teach
#             queryset = Question.objects.filter(assignment__course__teacher=self.request.user)
        
#         elif self.request.user.is_student:
#             # Students can see only questions from assignments in their courses
#             queryset = Question.objects.filter(assignment__course__enrollments__student=self.request.user)

#         # Optional: If assignment_id is provided, filter by it
#         assignment_id = self.request.query_params.get('assignment_id')
#         if assignment_id:
#             queryset = queryset.filter(assignment_id=assignment_id)

#         return queryset

    
class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseEnrollmentWriteSerializer
        return CourseEnrollmentReadSerializer  # To return course details for enrolled courses

    def perform_create(self, serializer):
        # Ensure only students can enroll in courses
        if not self.request.user.is_student:
            raise PermissionDenied("Only students can enroll in courses.")
        
        # Get course ID from request data
        course_id = self.request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        # Check if the student is already enrolled in the course
        if CourseEnrollment.objects.filter(course=course, student=self.request.user).exists():
            raise PermissionDenied("You are already enrolled in this course.")
        
        # Create the enrollment for the student in the selected course
        serializer.save(course=course, student=self.request.user)

    def get_queryset(self):
        # Return the courses the student has enrolled in
        if self.request.user.is_student:
            return CourseEnrollment.objects.filter(student=self.request.user)
        elif self.request.user.is_teacher:
            return CourseEnrollment.objects.filter(course__teacher=self.request.user).order_by('id')
        return CourseEnrollment.objects.none()
    

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SubmissionWriteSerializer
        return SubmissionReadSerializer

    def perform_create(self, serializer):
        # Ensure the student hasn't already submitted an answer for this question
        if Submission.objects.filter(assignment=serializer.validated_data['assignment'], student=self.request.user).exists():
            raise PermissionDenied("You have already submitted an answer for this question.")
        
        # Save the submission with the current student
        serializer.save(student=self.request.user)

    def update(self, request, *args, **kwargs):
        # Retrieve the submission instance
        submission = self.get_object()

        # Prevent update if the submission is graded
        if submission.is_graded:
            raise PermissionDenied("You cannot update a submission that has already been graded.")
        
        # if submission.is_final and self.request.user.is_student:
        #     raise PermissionDenied("You cannot update a submission after it has been finalized.")

        # if not submission.is_final and self.request.user.is_teacher:
        #     raise PermissionDenied("You can only update a submission after the student has finalized it.")

        
        # Optionally, prevent update after a certain period of time or after a deadline
        # Example: check assignment deadline or time of submission
        if submission.submitted_at and submission.submitted_at > submission.assignment.deadline:
            raise PermissionDenied("You cannot update a submission after the assignment deadline.")

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        # Return submissions for the logged-in student
        if self.request.user.is_student:
            return Submission.objects.filter(student=self.request.user)
        # Teachers can view submissions related to their assignments
        elif self.request.user.is_teacher:
            return Submission.objects.filter(assignment__course__teacher=self.request.user)
        return Submission.objects.none()
    
    def list(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_student:
            # Get distinct assignments where the current student has submitted work
            assignments = Assignment.objects.filter(submissions__student=user).distinct()
        elif user.is_teacher:
            # Get distinct assignments where the teacher is the owner of the course
            assignments = Assignment.objects.filter(course__teacher=user).distinct()
        else:
            return Response({"detail": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        
        course_id = self.request.query_params.get('course_id')
        if course_id:
            assignments = assignments.filter(course_id=course_id)

        # Serialize the assignments and their related submissions
        serializer = AssignmentWithSubmissionsSerializer(assignments, many=True)

        # Return the custom response, which is grouped by assignment
        return Response(serializer.data)
    
    # @action(detail=False, methods=['post'], url_path='final-submit')
    # def final_submit(self, request, *args, **kwargs):
    #     """
    #     Mark all submissions for an assignment as final, preventing further changes.
    #     """
    #     student = request.user
    #     assignment_id = request.data.get('assignment_id')

    #     # Ensure that the student has submissions for the given assignment
    #     submissions = Submission.objects.filter(
    #         student=student, 
    #         question__assignment_id=assignment_id
    #     )

    #     if not submissions.exists():
    #         return Response({"detail": "No submissions found for this assignment."}, status=status.HTTP_404_NOT_FOUND)

    #     # Mark all submissions as final
    #     submissions.update(is_final=True)

    #     return Response({"detail": "Submission has been marked as final. No further changes allowed."}, status=status.HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = {}

        # If the logged-in user is a student
        if request.user.is_student:
            # Enrolled courses for the student
            enrolled_courses = Course.objects.filter(enrollments__student=request.user).distinct()

            # Completed courses where all assignments are submitted
            completed_courses = Course.objects.filter(
                enrollments__student=request.user,
                assignments__submissions__student=request.user,
            ).distinct()


            # Calculate average rating across all submitted assignments
            average_rating = Submission.objects.filter(
                student=request.user,
                grade__isnull=False
            ).aggregate(Avg('grade'))['grade__avg']

            payload['enrolled_courses'] = enrolled_courses.count()
            payload['completed_courses'] = completed_courses.count()
            payload['average_rating'] = average_rating if average_rating else 0

        # If the logged-in user is a teacher
        elif request.user.is_teacher:
            # Active courses (courses that have assignments with deadlines in the future)
            active_courses = Course.objects.filter(
                teacher=request.user,
                assignments__deadline__gt=timezone.now()
            ).distinct()

            # Total courses taught by the teacher
            total_courses = Course.objects.filter(teacher=request.user).count()

            # Total unique students enrolled in the teacher's courses
            total_students = User.objects.filter(
                is_student=True,
                enrollments__course__teacher=request.user
            ).distinct().count()

            payload['active_courses'] = active_courses.count()
            payload['total_courses'] = total_courses
            payload['total_students'] = total_students

        return Response(payload)


class View(APIView):
    permission_classes = [IsAuthenticated]