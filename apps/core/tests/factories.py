# apps/core/tests/factories.py
import factory
from django.contrib.auth.models import User

from apps.core.models import (
    Course,
    Instructor,
    InstructorShift,
    InstructorSkill,
    Reservation,
    School,
    Student,
    TimeSlot,
    Progress,
)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Sequence(lambda n: f"テスト教室{n}")


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"テスト講座{n}")
    description = "テスト用の講座です"
    duration_weeks = 8


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeSlot

    slot_number = factory.Sequence(lambda n: n + 1)
    start_time = "09:00:00"
    end_time = "10:00:00"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"testuser{n}")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save()


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"テスト生徒{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.user.username}@example.com")
    school = factory.SubFactory(SchoolFactory)
    enrollment_year = 2025
    age = 12
    grade = "小学校6年生"
    status = "active"


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    name = factory.Sequence(lambda n: f"テスト講師{n}")
    email = factory.Sequence(lambda n: f"instructor{n}@example.com")
    school = factory.SubFactory(SchoolFactory)
    tenure_years = 3
    status = "active"


class InstructorSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InstructorSkill

    instructor = factory.SubFactory(InstructorFactory)
    course = factory.SubFactory(CourseFactory)


class InstructorShiftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InstructorShift

    instructor = factory.SubFactory(InstructorFactory)
    shift_date = "2026-03-01"
    slot = factory.SubFactory(TimeSlotFactory)
    status = "open"


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    student = factory.SubFactory(StudentFactory)
    instructor_shift = factory.SubFactory(InstructorShiftFactory)
    course = factory.SubFactory(CourseFactory)
    status = "pending"


class ProgressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Progress

    student = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)
    status = "not_started"
