# apps/core/models/instructor_skill.py
from django.db import models
from simple_history.models import HistoricalRecords


class InstructorSkill(models.Model):
    instructor = models.ForeignKey("Instructor", on_delete=models.CASCADE, related_name="skills")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="skilled_instructors")
    history = HistoricalRecords()

    class Meta:
        db_table = "instructor_skills"
        verbose_name = "講師スキル"
        verbose_name_plural = "講師スキル"
        constraints = [
            models.UniqueConstraint(
                fields=["instructor", "course"],
                name="unique_instructor_skill",
            )
        ]

    def __str__(self):
        return f"{self.instructor.name} - {self.course.title}"