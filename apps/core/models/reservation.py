# apps/core/models/reservation.py
from django.db import models


class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "確定"
        CANCELLED = "cancelled", "キャンセル"
        PENDING = "pending", "仮予約"

    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="reservations")
    instructor_shift = models.ForeignKey("InstructorShift", on_delete=models.PROTECT, related_name="reservations")
    course = models.ForeignKey("Course", on_delete=models.PROTECT, related_name="reservations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"{self.student.name} - {self.course.title} ({self.status})"