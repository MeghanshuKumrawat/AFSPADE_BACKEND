from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, QuestionViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'questions', QuestionViewSet, basename='questions')

urlpatterns = [
    # Other paths
] + router.urls
