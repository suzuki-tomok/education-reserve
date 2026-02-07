# apps/core/api/views/course.py
from rest_framework import viewsets

from apps.core.models import Course
from apps.core.api.serializers import CourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer