# apps/core/admin/time_slot.py
from django.contrib import admin

from apps.core.models import TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "slot_number", "start_time", "end_time")
    list_display_links = ("id", "slot_number")
    ordering = ("slot_number",)
