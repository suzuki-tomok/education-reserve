# apps/core/api/views/survey.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.models import StudentSurvey
from apps.core.api.serializers import SurveyCreateSerializer


class SurveyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentSurvey.objects.all()
    serializer_class = SurveyCreateSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
