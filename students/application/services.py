from dataclasses import dataclass
from typing import Any

from django.db import transaction

from students.domain.policies import (
    cancel_enrollment as apply_cancel_enrollment,
    reactivate_cancelled_enrollment,
)
from students.infrastructure.repositories import DjangoStudentRepository


@dataclass(frozen=True)
class EnrollmentResult:
    enrollment: Any
    created: bool = False
    reactivated: bool = False


def get_or_create_student(user, repository=None):
    return (repository or DjangoStudentRepository()).get_or_create_student(user)


@transaction.atomic
def enroll_student(student, course, repository=None):
    repository = repository or DjangoStudentRepository()
    enrollment = repository.find_enrollment(student, course)

    if enrollment is None:
        return EnrollmentResult(
            enrollment=repository.enroll(student, course),
            created=True,
        )

    if reactivate_cancelled_enrollment(enrollment):
        repository.save_enrollment(enrollment, fields=["status"])
        return EnrollmentResult(enrollment=enrollment, reactivated=True)

    return EnrollmentResult(enrollment=enrollment)


@transaction.atomic
def cancel_enrollment(enrollment, repository=None):
    apply_cancel_enrollment(enrollment)
    (repository or DjangoStudentRepository()).save_enrollment(
        enrollment,
        fields=["status"],
    )
    return enrollment
