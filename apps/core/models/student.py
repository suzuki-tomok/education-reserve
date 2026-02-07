# apps/core/models/student.py
from django.db import models


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "在籍"
        INACTIVE = "inactive", "退会"
        SUSPENDED = "suspended", "休会"

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    school = models.ForeignKey("School", on_delete=models.PROTECT, related_name="students")
    enrollment_year = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=50, blank=True, default="")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "students"

    def __str__(self):
        return self.name