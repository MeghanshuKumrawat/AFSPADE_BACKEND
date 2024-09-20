from django.urls import path
from accounts.views import LoginView, SignupView, UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', SignupView.as_view(), name='signup'),
    path('user', UserView.as_view(), name='user'),
] + router.urls
