from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from rest_framework.permissions import AllowAny


class UserCreateAPIView(generics.CreateAPIView):
    """Представление для создания нового пользователя"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    """Представление для аутентификации пользователя"""

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST запрос с данными пользователя"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
