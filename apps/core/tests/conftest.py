# apps/core/tests/conftest.py
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.core.tests.factories import (
    StudentFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def auth_client(student):
    """認証済みAPIクライアント"""
    client = APIClient()
    token = Token.objects.create(user=student.user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client
