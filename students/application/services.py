from dataclasses import dataclass

from django.db import transaction

from students.infrastructure.repositories import DjangoStudentRepository
from students.models import Matricula


@dataclass(frozen=True)
class EnrollmentResult:
    enrollment: Matricula
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

    if enrollment.status == Matricula.Status.CANCELADA:
        enrollment.status = Matricula.Status.ATIVA
        repository.save_enrollment(enrollment, fields=["status"])
        return EnrollmentResult(enrollment=enrollment, reactivated=True)

    return EnrollmentResult(enrollment=enrollment)


@transaction.atomic
def cancel_enrollment(enrollment, repository=None):
    enrollment.status = Matricula.Status.CANCELADA
    (repository or DjangoStudentRepository()).save_enrollment(
        enrollment,
        fields=["status"],
    )
    return enrollment
