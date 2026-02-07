# apps/core/models/school.py
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "schools"

    def __str__(self):
        return self.name