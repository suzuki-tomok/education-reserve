# apps/core/api/views/__init__.py
from .course import CourseViewSet
from .shift import ShiftViewSet
from .reservation import ReservationViewSet
from .progress import ProgressViewSet
from .survey import SurveyViewSet
from .auth import LoginView, MeView