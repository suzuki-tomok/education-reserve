# apps/core/admin/progress.py
from django.contrib import admin

from apps.core.models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course", "instructor", "status", "last_updated")
    list_display_links = ("id", "student")
    list_filter = ("status", "course")
    search_fields = ("student__name",)
