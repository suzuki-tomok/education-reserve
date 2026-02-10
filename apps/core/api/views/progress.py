# apps/core/api/views/progress.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.models import Progress
from apps.core.api.serializers import ProgressSerializer


class ProgressViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer
    ordering = ["-id"]

    def get_queryset(self):
        return (
            Progress.objects.filter(student=self.request.user.student)
            .select_related("course", "instructor")
        )