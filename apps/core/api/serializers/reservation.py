# apps/core/api/serializers/reservation.py
from rest_framework import serializers

from apps.core.models import Reservation
from apps.core.api.serializers.shift import ShiftSerializer
from apps.core.api.serializers.course import CourseSerializer


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "instructor_shift", "course")

    def validate_instructor_shift(self, value):
        if value.status != "open":
            raise serializers.ValidationError("このシフトは出勤ではありません。")
        if value.reservations.filter(status__in=["pending", "confirmed"]).exists():
            raise serializers.ValidationError("このシフトはすでに予約が入っています。")
        return value

    def validate(self, data):
        shift = data["instructor_shift"]
        course = data["course"]
        if not shift.instructor.skills.filter(course=course).exists():
            raise serializers.ValidationError("この講師はこの講座を担当できません。")
        return data


class ReservationListSerializer(serializers.ModelSerializer):
    instructor_shift = ShiftSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "instructor_shift", "course", "status")
