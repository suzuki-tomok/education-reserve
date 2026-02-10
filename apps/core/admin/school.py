# apps/core/admin/school.py
from django.contrib import admin

from apps.core.models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
