# apps/core/admin/reservation.py
from django.contrib import admin

from apps.core.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "get_instructor", "course", "get_date", "status")
    list_display_links = ("id", "student")
    list_filter = ("status", "course")
    search_fields = ("student__name",)
    actions = ["mark_confirmed", "mark_cancelled"]

    @admin.display(description="講師")
    def get_instructor(self, obj):
        return obj.instructor_shift.instructor.name

    @admin.display(description="日時")
    def get_date(self, obj):
        shift = obj.instructor_shift
        return f"{shift.shift_date} {shift.slot}"

    @admin.action(description="選択した予約を確定にする")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="選択した予約をキャンセルにする")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="cancelled")