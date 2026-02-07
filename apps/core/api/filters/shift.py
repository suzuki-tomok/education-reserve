# apps/core/api/filters/shift.py
from django_filters import rest_framework as filters

from apps.core.models import InstructorShift


class ShiftFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="shift_date")
    course_id = filters.NumberFilter(method="filter_by_course")

    class Meta:
        model = InstructorShift
        fields = ("date", "course_id")

    def filter_by_course(self, queryset, name, value):
        return queryset.filter(instructor__skills__course_id=value)