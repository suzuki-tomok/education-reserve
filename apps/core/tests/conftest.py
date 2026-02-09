# apps/core/tests/conftest.py
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.core.tests.factories import (
    CourseFactory,
    InstructorFactory,
    SchoolFactory,
    StudentFactory,
    TimeSlotFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def school():
    return SchoolFactory()


@pytest.fixture
def course():
    return CourseFactory()


@pytest.fixture
def time_slot():
    return TimeSlotFactory()


@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def instructor():
    return InstructorFactory()


@pytest.fixture
def auth_client(student):
    """認証済みAPIクライアント"""
    client = APIClient()
    token = Token.objects.create(user=student.user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client