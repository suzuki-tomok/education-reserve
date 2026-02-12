# apps/core/tests/test_api.py
import pytest

from apps.core.tests.factories import (
    CourseFactory,
    InstructorFactory,
    InstructorShiftFactory,
    InstructorSkillFactory,
    ReservationFactory,
    StudentFactory,
    ProgressFactory,
    TimeSlotFactory,
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

    def test_same_student_same_timeslot(self, auth_client, student):
        slot = TimeSlotFactory()
        course1 = CourseFactory()
        course2 = CourseFactory()

        instructor1 = InstructorFactory()
        instructor2 = InstructorFactory()
        InstructorSkillFactory(instructor=instructor1, course=course1)
        InstructorSkillFactory(instructor=instructor2, course=course2)

        shift1 = InstructorShiftFactory(
            instructor=instructor1, slot=slot, shift_date="2026-03-01", status="open"
        )
        shift2 = InstructorShiftFactory(
            instructor=instructor2, slot=slot, shift_date="2026-03-01", status="open"
        )

        # 1件目：成功
        auth_client.post(
            "/api/reservations/",
            {"instructor_shift": shift1.id, "course": course1.id},
        )

        # 2件目：同じ時間帯 → 弾かれるべき
        response = auth_client.post(
            "/api/reservations/",
            {"instructor_shift": shift2.id, "course": course2.id},
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestProgress:
    def test_list_progress(self, auth_client):
        response = auth_client.get("/api/progress/")
        assert response.status_code == 200

    def test_unauthenticated(self, api_client):
        response = api_client.get("/api/progress/")
        assert response.status_code == 401

    def test_cannot_see_others_progress(self, auth_client, student):
        ProgressFactory()  # 別の生徒の進捗
        response = auth_client.get("/api/progress/")
        assert response.status_code == 200
        assert response.data["count"] == 0


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

    def test_survey_pending_reservation_rejected(self, auth_client, student):
        course = CourseFactory()
        shift = InstructorShiftFactory()
        reservation = ReservationFactory(
            student=student,
            instructor_shift=shift,
            course=course,
            status="pending",
        )
        response = auth_client.post(
            "/api/surveys/",
            {
                "reservation": reservation.id,
                "rating": 5,
                "comment": "良かった",
            },
        )
        assert response.status_code == 400
