import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserViews:
    """Тестовый класс проверяет работу UserViews"""

    def test_user_create(self, api_client, user_data):
        """Тест успешного создания нового пользователя"""
        url = reverse('register')
        response = api_client.post(url, user_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=user_data['email']).exists()

    def test_user_login(self, api_client):
        """Тест успешного логина пользователя"""
        user = UserFactory.create()

        url = reverse('login')
        login_data = {
            'email': user.email,
            'password': 'testpassword123'
        }

        response = api_client.post(url, login_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == login_data['email']
        assert 'refresh' and 'access' in response.data['tokens']

    def test_user_create_existing_email(self, api_client, user_data):
        """Тест неуспешного создания пользователя с уже существующим email"""
        UserFactory.create(email=user_data['email'])

        url = reverse('register')
        response = api_client.post(url, user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_user_create_missing_password(self, api_client, user_data):
        """Тест неуспешного создания пользователя без пароля"""
        user_data.pop('password')

        url = reverse('register')
        response = api_client.post(url, user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_user_login_wrong_password(self, api_client):
        """Тест неуспешного логина с неправильным паролем"""
        user = UserFactory.create()
        url = reverse('login')
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data
