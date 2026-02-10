# apps/core/admin/course.py
from django.contrib import admin

from apps.core.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "duration_weeks")
    list_display_links = ("id", "title")
    search_fields = ("title",)
