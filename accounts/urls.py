from django.urls import path
from accounts.views import LoginView, SignupView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', SignupView.as_view(), name='signup'),
]
