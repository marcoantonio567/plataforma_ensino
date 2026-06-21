from dataclasses import dataclass
from typing import Any

from django.db import transaction

from students.domain.policies import (
    cancel_enrollment as apply_cancel_enrollment,
    reactivate_cancelled_enrollment,
)
from students.infrastructure.repositories import DjangoEnrollmentRepository


@dataclass(frozen=True)
class EnrollmentResult:
    enrollment: Any
    created: bool = False
    reactivated: bool = False


def get_or_create_student(user, repository=None):
    return (repository or DjangoEnrollmentRepository()).get_or_create_student(user)


@transaction.atomic
def enroll_student(student, course, repository=None):
    repository = repository or DjangoEnrollmentRepository()
    enrollment = repository.find_by_student_and_course(student, course)

    if enrollment is None:
        return EnrollmentResult(
            enrollment=repository.add(student, course),
            created=True,
        )

    if reactivate_cancelled_enrollment(enrollment):
        repository.save(enrollment, fields=["status"])
        return EnrollmentResult(enrollment=enrollment, reactivated=True)

    return EnrollmentResult(enrollment=enrollment)


@transaction.atomic
def cancel_enrollment(enrollment, repository=None):
    apply_cancel_enrollment(enrollment)
    (repository or DjangoEnrollmentRepository()).save(
        enrollment,
        fields=["status"],
    )
    return enrollment
