# apps/core/api/views/progress.py
from rest_framework import viewsets, mixins

from apps.core.models import Progress
from apps.core.api.serializers import ProgressSerializer


class ProgressViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProgressSerializer

    def get_queryset(self):
        student_id = self.request.query_params.get("student_id")
        if student_id:
            return (
                Progress.objects.filter(student_id=student_id)
                .select_related("course", "instructor")
            )
        return Progress.objects.none()