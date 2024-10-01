from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CourseViewSet, AssignmentViewSet, QuestionViewSet, CourseEnrollmentViewSet, SubmissionViewSet, DashboardView

router = DefaultRouter(trailing_slash=False)
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'enrollments', CourseEnrollmentViewSet, basename='course-enrollment')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    # Other paths
    path('dashboard', DashboardView.as_view(), name='dashboard'),

] + router.urls
