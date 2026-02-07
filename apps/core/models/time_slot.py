# apps/core/models/time_slot.py
from django.db import models


class TimeSlot(models.Model):
    slot_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "time_slots"

    def __str__(self):
        return f"{self.slot_number}限 ({self.start_time}〜{self.end_time})"