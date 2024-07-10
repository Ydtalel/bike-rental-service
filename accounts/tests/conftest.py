import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Возвращает экземпляр класса APIClient"""
    return APIClient()


@pytest.fixture
def user_data():
    """Возвращает данные пользователя"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'name': 'Test User'
    }
