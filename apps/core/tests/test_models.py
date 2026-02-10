# apps/core/tests/test_models.py
import pytest
from django.db import IntegrityError

from apps.core.tests.factories import (
    CourseFactory,
    InstructorFactory,
    InstructorShiftFactory,
    InstructorSkillFactory,
    ReservationFactory,
    SchoolFactory,
    StudentFactory,
    TimeSlotFactory,
)


@pytest.mark.django_db
class TestSchool:
    def test_str(self):
        school = SchoolFactory(name="自由が丘教室")
        assert str(school) == "自由が丘教室"

    def test_unique_name(self):
        SchoolFactory(name="自由が丘教室")
        with pytest.raises(IntegrityError):
            SchoolFactory(name="自由が丘教室")


@pytest.mark.django_db
class TestCourse:
    def test_str(self):
        course = CourseFactory(title="Python入門")
        assert str(course) == "Python入門"


@pytest.mark.django_db
class TestTimeSlot:
    def test_str(self):
        slot = TimeSlotFactory(
            slot_number=1, start_time="09:00:00", end_time="10:00:00"
        )
        assert "1限" in str(slot)


@pytest.mark.django_db
class TestStudent:
    def test_str(self):
        student = StudentFactory(name="鈴木一郎")
        assert str(student) == "鈴木一郎"

    def test_unique_email(self):
        StudentFactory(email="test@example.com")
        with pytest.raises(IntegrityError):
            StudentFactory(email="test@example.com")

    def test_default_status(self):
        student = StudentFactory()
        assert student.status == "active"


@pytest.mark.django_db
class TestInstructor:
    def test_str(self):
        instructor = InstructorFactory(name="田中太郎")
        assert str(instructor) == "田中太郎"

    def test_default_status(self):
        instructor = InstructorFactory()
        assert instructor.status == "active"


@pytest.mark.django_db
class TestInstructorSkill:
    def test_str(self):
        skill = InstructorSkillFactory(
            instructor=InstructorFactory(name="田中太郎"),
            course=CourseFactory(title="Python入門"),
        )
        assert str(skill) == "田中太郎 - Python入門"

    def test_unique_constraint(self):
        skill = InstructorSkillFactory()
        with pytest.raises(IntegrityError):
            InstructorSkillFactory(
                instructor=skill.instructor,
                course=skill.course,
            )


@pytest.mark.django_db
class TestInstructorShift:
    def test_str(self):
        shift = InstructorShiftFactory()
        assert str(shift)

    def test_default_status_closed(self):
        shift = InstructorShiftFactory(status="closed")
        assert shift.status == "closed"

    def test_unique_constraint(self):
        shift = InstructorShiftFactory()
        with pytest.raises(IntegrityError):
            InstructorShiftFactory(
                instructor=shift.instructor,
                shift_date=shift.shift_date,
                slot=shift.slot,
            )


@pytest.mark.django_db
class TestReservation:
    def test_str(self):
        reservation = ReservationFactory(
            student=StudentFactory(name="鈴木一郎"),
            course=CourseFactory(title="Python入門"),
        )
        assert "鈴木一郎" in str(reservation)
        assert "Python入門" in str(reservation)

    def test_default_status_pending(self):
        reservation = ReservationFactory()
        assert reservation.status == "pending"
