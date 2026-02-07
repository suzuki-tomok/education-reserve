# apps/core/models/school.py
from django.db import models
from simple_history.models import HistoricalRecords


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "schools"
        verbose_name = "学校"
        verbose_name_plural = "学校"

    def __str__(self):
        return self.name