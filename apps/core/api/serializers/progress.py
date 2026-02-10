# apps/core/api/serializers/progress.py
from rest_framework import serializers

from apps.core.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    instructor_name = serializers.CharField(source="instructor.name", read_only=True)

    class Meta:
        model = Progress
        fields = (
            "id",
            "course_title",
            "instructor_name",
            "status",
            "note",
            "last_updated",
        )
