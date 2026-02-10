# apps/core/api/views/reservation.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.models import Reservation
from apps.core.api.serializers import ReservationCreateSerializer, ReservationListSerializer


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    ordering = ["-id"]

    def get_queryset(self):
        return (
            Reservation.objects.filter(student=self.request.user.student)
            .select_related("instructor_shift__instructor", "instructor_shift__slot", "course")
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationListSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)