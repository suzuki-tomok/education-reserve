# apps/core/api/serializers/auth.py
from rest_framework import serializers

from apps.core.models import Student


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "name", "email", "school", "grade", "status")