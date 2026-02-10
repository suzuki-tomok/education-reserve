# apps/core/api/views/shift.py
from rest_framework import viewsets, mixins

from apps.core.models import InstructorShift
from apps.core.api.serializers import ShiftSerializer
from apps.core.api.filters import ShiftFilter


class ShiftViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ShiftSerializer
    filterset_class = ShiftFilter
    ordering = ["-id"]

    def get_queryset(self):
        return (
            InstructorShift.objects.filter(status="open")
            .exclude(
                reservations__status__in=["pending", "confirmed"]
            )
            .select_related("instructor", "slot")
        )