from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView 
from rest_framework.decorators import action, api_view
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse
from accounts.models import User
from accounts.serializers import LoginSerializer, SignupSerializer, UserReadSerializer, UserWriteSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens upon successful login, including user role in the response.
    Checks if the user's email is verified before allowing login.
    """

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            
            # Check if the email is verified
            if not user.is_active:
                return Response({'detail': 'Email is not verified. Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Verify the password
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                role = 'student' if user.is_student else 'teacher' if user.is_teacher else 'admin'

                return Response({
                    'role': role,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)  # Optionally include refresh token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                
class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get("email"))
        if not user.exists():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                # Generate token and encode UID
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                # Build verification URL
                verification_url = (
                    request.data.get("frontend_url")
                    + "/api/auth/verify-email/"
                    + uidb64
                    + "/"
                    + token
                )
                print(verification_url)
                # Send verification email
                subject = "Verify your email address"
                message = f"Please click the link below to verify your email address:\n{verification_url}"
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return Response({"detail": "User created successfully. Check your email to verify your account."},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = user.first()
            # Generate token and encode UID
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Build verification URL
            verification_url = (
                request.data.get("frontend_url")
                + "/api/auth/verify-email/"
                + uidb64
                + "/"
                + token
            )
            print(verification_url)

            # Send verification email
            subject = "Verify your email address"
            message = f"Please click the link below to verify your email address:\n{verification_url}"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"detail": "Verification email sent"},
                            status=status.HTTP_201_CREATED)

        
class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check if the token is valid
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user
            user.save()
            return Response({"detail": "Email verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Assuming you want to handle updates here
        user = request.user
        serializer = UserWriteSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


User = get_user_model()

class PasswordResetView(APIView):

    def validate_password_reset_link(self, request, uidb64, token):
        """
        Validate the password reset link by decoding the user ID and verifying the token.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Valid reset link!", "email": user.email},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid reset link!"}, status=status.HTTP_400_BAD_REQUEST
            )

    def send_password_reset_link(self, request):
        """
        Send a password reset link to the user via email.
        """
        email = str(request.data.get("email")).lower()
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = (
            request.data.get("frontend_url")
            + "/password-reset/confirm/"
            + uidb64
            + "/"
            + token
        )
        print(reset_link, "------------")  # For debugging purposes

        # Send the email with the reset link
        response = send_mail(
            subject="Password Reset Link",
            message=f"Please use the following link to reset your password:\n{reset_link}",
            from_email=None,  # Replace with your default from email in settings
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response({"detail": "Email sent!"}, status=status.HTTP_200_OK)

    def reset_password(self, request, uidb64, token):
        """
        Handle the actual password reset form submission.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                user.is_active = True
                user.save()
                return Response(
                    {"detail": "Password reset successfully!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": form.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail": "Invalid reset link!"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests. This method will delegate the request to the appropriate action based on the URL path.
        """
        action = request.data.get("action")

        if action == "send_password_reset_link":
            return self.send_password_reset_link(request)
        elif action == "reset_password":
            uidb64 = request.data.get("uidb64")
            token = request.data.get("token")
            return self.reset_password(request, uidb64, token)
        elif action == "validate_reset_link":
            uidb64 = request.data.get("uidb64")
            token = request.data.get("token")
            return self.validate_password_reset_link(request, uidb64, token)
        else:
            return Response(
                {"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )

    
@api_view(['POST'])
def send_test_email(request):
    try:
        # Send the email
        send_mail(
            subject='Test Email',
            message='This is a test email from Django API.',
            from_email='afspade@netdaplimited.com',
            recipient_list=['meghanshukumrawat16@gmail.com'],  # Add the recipient email
            fail_silently=False,
        )
        
        # Return success response
        return Response({"message": "Test email sent successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)