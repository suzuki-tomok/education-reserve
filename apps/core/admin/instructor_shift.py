# apps/core/admin/instructor_shift.py
from django.contrib import admin

from apps.core.models import InstructorShift


@admin.register(InstructorShift)
class InstructorShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "instructor", "shift_date", "slot", "status")
    list_display_links = ("id", "instructor")
    list_editable = ("status",)
    list_filter = ("status", "shift_date", "instructor")
    date_hierarchy = "shift_date"
    actions = ["mark_open", "mark_closed"]

    @admin.action(description="選択したシフトを出勤にする")
    def mark_open(self, request, queryset):
        queryset.update(status="open")

    @admin.action(description="選択したシフトを休みにする")
    def mark_closed(self, request, queryset):
        queryset.update(status="closed")