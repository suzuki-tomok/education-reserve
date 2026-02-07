# apps/core/api/serializers/shift.py
from rest_framework import serializers

from apps.core.models import InstructorShift


class ShiftSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source="instructor.name", read_only=True)
    slot_number = serializers.IntegerField(source="slot.slot_number", read_only=True)
    start_time = serializers.TimeField(source="slot.start_time", read_only=True)
    end_time = serializers.TimeField(source="slot.end_time", read_only=True)

    class Meta:
        model = InstructorShift
        fields = (
            "id",
            "instructor_name",
            "shift_date",
            "slot_number",
            "start_time",
            "end_time",
        )