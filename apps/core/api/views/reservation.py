# apps/core/api/views/reservation.py
from rest_framework import viewsets, mixins

from apps.core.models import Reservation
from apps.core.api.serializers import ReservationCreateSerializer, ReservationListSerializer


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    def get_queryset(self):
        student_id = self.request.query_params.get("student_id")
        if student_id:
            return (
                Reservation.objects.filter(student_id=student_id)
                .select_related("instructor_shift__instructor", "instructor_shift__slot", "course")
                .order_by("-id")
            )
        return Reservation.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationListSerializer

    def perform_create(self, serializer):
        student_id = self.request.query_params.get("student_id")
        serializer.save(student_id=student_id)