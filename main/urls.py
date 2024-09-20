from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, QuestionViewSet, CourseEnrollmentViewSet, SubmissionViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'enrollments', CourseEnrollmentViewSet, basename='course-enrollment')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    # Other paths
] + router.urls
