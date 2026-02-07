# apps/core/models/course.py
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    duration_weeks = models.PositiveIntegerField()

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.title