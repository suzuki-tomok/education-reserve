# apps/core/models/instructor.py
from django.db import models


class Instructor(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "在籍"
        INACTIVE = "inactive", "退職"

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    school = models.ForeignKey("School", on_delete=models.PROTECT, related_name="instructors")
    tenure_years = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "instructors"

    def __str__(self):
        return self.name