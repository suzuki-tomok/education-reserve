# apps/core/api/serializers/auth.py
from rest_framework import serializers

from apps.core.models import Student


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MeSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)

    class Meta:
        model = Student
        fields = ("id", "name", "email", "school_name", "grade", "status")