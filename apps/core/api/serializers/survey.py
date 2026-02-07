# apps/core/api/serializers/survey.py
from rest_framework import serializers

from apps.core.models import StudentSurvey


class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSurvey
        fields = ("id", "reservation", "rating", "comment")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("評価は1〜5の範囲で入力してください。")
        return value

    def validate_reservation(self, value):
        if value.status != "confirmed":
            raise serializers.ValidationError("確定済みの予約のみアンケート回答できます。")
        if hasattr(value, "survey"):
            raise serializers.ValidationError("この予約にはすでにアンケートが回答済みです。")
        return value