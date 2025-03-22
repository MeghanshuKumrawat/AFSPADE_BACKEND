from django.urls import path
from accounts.views import LoginView, SignupView, UserView, EmailVerificationView, PasswordResetView, send_test_email
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', SignupView.as_view(), name='signup'),
    path('verify-email/<uidb64>/<token>', EmailVerificationView.as_view(), name='email-verification'),
    path('password-reset', PasswordResetView.as_view(), name='password-reset'),
    path('user', UserView.as_view(), name='user'),
    path('send-test-email', send_test_email, name='send_test_email'),
] + router.urls
