# apps/core/models/instructor_shift.py
from django.db import models
from simple_history.models import HistoricalRecords


class InstructorShift(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "出勤"
        CLOSED = "closed", "休み"

    instructor = models.ForeignKey("Instructor", on_delete=models.CASCADE, related_name="shifts")
    shift_date = models.DateField()
    slot = models.ForeignKey("TimeSlot", on_delete=models.CASCADE, related_name="shifts")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CLOSED)
    history = HistoricalRecords()

    class Meta:
        db_table = "instructor_shifts"
        verbose_name = "シフト"
        verbose_name_plural = "シフト"
        constraints = [
            models.UniqueConstraint(
                fields=["instructor", "shift_date", "slot"],
                name="unique_instructor_shift",
            )
        ]

    def __str__(self):
        return f"{self.instructor.name} {self.shift_date} {self.slot}"