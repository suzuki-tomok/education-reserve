# apps/core/admin/instructor.py
from django.contrib import admin

from apps.core.models import Instructor, InstructorSkill


class InstructorSkillInline(admin.TabularInline):
    model = InstructorSkill
    extra = 1


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "school", "tenure_years", "status")
    list_display_links = ("id", "name")
    list_filter = ("status", "school")
    search_fields = ("name", "email")
    inlines = [InstructorSkillInline]
