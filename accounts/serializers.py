from rest_framework import serializers
from accounts.models import User

class LoginSerializer(serializers.Serializer):
    """
    Login Serializer
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'matriculation_number', 'level', 'semester', 'is_student', 'is_teacher', 'image']
        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'required': False}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username'),
            phone=validated_data.get('phone'),
            matriculation_number=validated_data.get('matriculation_number'),
            level=validated_data.get('level'),
            semester=validated_data.get('semester'),
            is_student=validated_data.get('is_student', False),
            is_teacher=validated_data.get('is_teacher', False),
            image=validated_data.get('image', 'profiles/default.png'),
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserReadSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'matriculation_number', 'level', 'semester', 'image', 'role']

    def get_role(self, obj):
        if obj.is_teacher:
            return 'teacher'
        elif obj.is_student:
            return 'student'
        return 'unknown'

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'matriculation_number', 'level', 'semester', 'image']
