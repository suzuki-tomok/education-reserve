# apps/core/admin/student.py
from django.contrib import admin

from apps.core.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "school", "grade", "status")
    list_display_links = ("id", "name")
    list_filter = ("status", "school", "enrollment_year")
    search_fields = ("name", "email")
