from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя (User)"""

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])

    def create(self, validated_data):
        """Создает нового пользователя на основе переданных данных"""
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Валидирует переданные данные пользователя"""
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                'Неверные учетные данные. Пожалуйста, попробуйте еще раз.')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {
            'email': user.email,
            'tokens': {'refresh': str(refresh), 'access': access_token}
        }
