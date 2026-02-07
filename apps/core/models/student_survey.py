# apps/core/models/student_survey.py
from django.db import models


class StudentSurvey(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="surveys")
    reservation = models.OneToOneField("Reservation", on_delete=models.CASCADE, related_name="survey")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, default="")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "student_surveys"
        verbose_name = "アンケート"
        verbose_name_plural = "アンケート"

    def __str__(self):
        return f"{self.student.name} - {self.rating}点"