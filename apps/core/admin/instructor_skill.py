# apps/core/admin/instructor_skill.py
from django.contrib import admin

from apps.core.models import InstructorSkill


@admin.register(InstructorSkill)
class InstructorSkillAdmin(admin.ModelAdmin):
    list_display = ("id", "instructor", "course")
    list_display_links = ("id", "instructor")
    list_filter = ("course",)
