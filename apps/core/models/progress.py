# apps/core/models/progress.py
from django.db import models


class Progress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "未着手"
        IN_PROGRESS = "in_progress", "進行中"
        COMPLETED = "completed", "完了"

    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="progress")
    instructor = models.ForeignKey("Instructor", on_delete=models.SET_NULL, null=True, related_name="progress")
    course = models.ForeignKey("Course", on_delete=models.PROTECT, related_name="progress")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    note = models.TextField(blank=True, default="")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "progress"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_progress",
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.course.title} ({self.status})"