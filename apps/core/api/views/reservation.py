# apps/core/api/views/reservation.py
from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.core.models import Reservation
from apps.core.api.serializers import (
    ReservationCreateSerializer,
    ReservationListSerializer,
)
from apps.core.models.instructor_shift import InstructorShift


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
            .select_related(
                "instructor_shift__instructor", "instructor_shift__slot", "course"
            )
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationListSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            shift = InstructorShift.objects.select_for_update().get(
                id=serializer.validated_data["instructor_shift"].id
            )

            if shift.status != "open":
                raise serializers.ValidationError("このシフトは出勤ではありません。")

            if shift.reservations.filter(status__in=["pending", "confirmed"]).exists():
                raise serializers.ValidationError(
                    "このシフトはすでに予約が入っています。"
                )

            serializer.save(student=self.request.user.student)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()

        if reservation.status not in ["pending", "confirmed"]:
            return Response(
                {"detail": "この予約はキャンセルできません。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.status = "cancelled"
        reservation.save()

        return Response({"detail": "キャンセルしました。"})
