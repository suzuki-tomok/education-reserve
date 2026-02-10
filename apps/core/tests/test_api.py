# apps/core/tests/test_api.py
import pytest

from apps.core.tests.factories import (
    CourseFactory,
    InstructorFactory,
    InstructorShiftFactory,
    InstructorSkillFactory,
    ReservationFactory,
    StudentFactory,
)


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client):
        student = StudentFactory()
        response = api_client.post(
            "/api/auth/login/",
            {
                "username": student.user.username,
                "password": "testpass123",
            },
        )
        assert response.status_code == 200
        assert "token" in response.data

    def test_login_wrong_password(self, api_client):
        student = StudentFactory()
        response = api_client.post(
            "/api/auth/login/",
            {
                "username": student.user.username,
                "password": "wrongpass",
            },
        )
        assert response.status_code == 401


@pytest.mark.django_db
class TestMe:
    def test_me_authenticated(self, auth_client, student):
        response = auth_client.get("/api/auth/me/")
        assert response.status_code == 200
        assert response.data["name"] == student.name

    def test_me_unauthenticated(self, api_client):
        response = api_client.get("/api/auth/me/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestCourses:
    def test_list_courses(self, auth_client):
        CourseFactory.create_batch(3)
        response = auth_client.get("/api/courses/")
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_retrieve_course(self, auth_client):
        course = CourseFactory(title="Python入門")
        response = auth_client.get(f"/api/courses/{course.id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Python入門"


@pytest.mark.django_db
class TestShifts:
    def test_list_shifts(self, auth_client):
        InstructorShiftFactory(status="open")
        response = auth_client.get("/api/shifts/")
        assert response.status_code == 200

    def test_filter_by_course_id(self, auth_client):
        course = CourseFactory()
        instructor = InstructorFactory()
        InstructorSkillFactory(instructor=instructor, course=course)
        InstructorShiftFactory(instructor=instructor, status="open")
        response = auth_client.get(f"/api/shifts/?course_id={course.id}")
        assert response.status_code == 200
        assert response.data["count"] == 1

    def test_closed_shifts_hidden(self, auth_client):
        InstructorShiftFactory(status="closed")
        response = auth_client.get("/api/shifts/")
        assert response.status_code == 200
        assert response.data["count"] == 0


@pytest.mark.django_db
class TestReservations:
    def test_create_reservation(self, auth_client, student):
        course = CourseFactory()
        instructor = InstructorFactory()
        InstructorSkillFactory(instructor=instructor, course=course)
        shift = InstructorShiftFactory(instructor=instructor, status="open")
        response = auth_client.post(
            "/api/reservations/",
            {
                "instructor_shift": shift.id,
                "course": course.id,
            },
        )
        assert response.status_code == 201

    def test_list_own_reservations(self, auth_client, student):
        course = CourseFactory()
        shift = InstructorShiftFactory()
        ReservationFactory(student=student, instructor_shift=shift, course=course)
        response = auth_client.get("/api/reservations/")
        assert response.status_code == 200
        assert response.data["count"] == 1

    def test_cannot_see_others_reservations(self, auth_client, student):
        ReservationFactory()  # 別の生徒の予約
        response = auth_client.get("/api/reservations/")
        assert response.status_code == 200
        assert response.data["count"] == 0

    def test_duplicate_reservation(self, auth_client, student):
        course = CourseFactory()
        instructor = InstructorFactory()
        InstructorSkillFactory(instructor=instructor, course=course)
        shift = InstructorShiftFactory(instructor=instructor, status="open")
        auth_client.post(
            "/api/reservations/",
            {
                "instructor_shift": shift.id,
                "course": course.id,
            },
        )
        response = auth_client.post(
            "/api/reservations/",
            {
                "instructor_shift": shift.id,
                "course": course.id,
            },
        )
        assert response.status_code == 400

    def test_closed_shift_reservation(self, auth_client):
        course = CourseFactory()
        instructor = InstructorFactory()
        InstructorSkillFactory(instructor=instructor, course=course)
        shift = InstructorShiftFactory(instructor=instructor, status="closed")
        response = auth_client.post(
            "/api/reservations/",
            {
                "instructor_shift": shift.id,
                "course": course.id,
            },
        )
        assert response.status_code == 400

    def test_no_skill_reservation(self, auth_client):
        course = CourseFactory()
        shift = InstructorShiftFactory(status="open")
        # InstructorSkillを作らない → スキルなし
        response = auth_client.post(
            "/api/reservations/",
            {
                "instructor_shift": shift.id,
                "course": course.id,
            },
        )
        assert response.status_code == 400

    def test_unauthenticated(self, api_client):
        response = api_client.get("/api/reservations/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestProgress:
    def test_list_progress(self, auth_client):
        response = auth_client.get("/api/progress/")
        assert response.status_code == 200

    def test_unauthenticated(self, api_client):
        response = api_client.get("/api/progress/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestSurveys:
    def test_create_survey(self, auth_client, student):
        course = CourseFactory()
        shift = InstructorShiftFactory()
        reservation = ReservationFactory(
            student=student,
            instructor_shift=shift,
            course=course,
            status="confirmed",
        )
        response = auth_client.post(
            "/api/surveys/",
            {
                "reservation": reservation.id,
                "rating": 5,
                "comment": "とても良かった",
            },
        )
        assert response.status_code == 201

    def test_unauthenticated(self, api_client):
        response = api_client.post("/api/surveys/", {})
        assert response.status_code == 401
