# apps/core/api/serializers/course.py
from rest_framework import serializers

from apps.core.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "description", "duration_weeks")