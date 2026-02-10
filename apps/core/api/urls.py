# apps/core/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.api.views import (
    CourseViewSet,
    ShiftViewSet,
    ReservationViewSet,
    ProgressViewSet,
    SurveyViewSet,
    LoginView,
    MeView,
)

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="course")
router.register("shifts", ShiftViewSet, basename="shift")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("progress", ProgressViewSet, basename="progress")
router.register("surveys", SurveyViewSet, basename="survey")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
