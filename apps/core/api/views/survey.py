# apps/core/api/views/survey.py
from rest_framework import viewsets, mixins

from apps.core.models import StudentSurvey
from apps.core.api.serializers import SurveyCreateSerializer


class SurveyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = StudentSurvey.objects.all()
    serializer_class = SurveyCreateSerializer

    def perform_create(self, serializer):
        student_id = self.request.query_params.get("student_id")
        serializer.save(student_id=student_id)