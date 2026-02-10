# apps/core/admin/student_survey.py
from django.contrib import admin

from apps.core.models import StudentSurvey


@admin.register(StudentSurvey)
class StudentSurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "reservation", "rating", "submitted_at")
    list_display_links = ("id", "student")
    list_filter = ("rating",)
    search_fields = ("student__name",)
    readonly_fields = ("submitted_at",)
