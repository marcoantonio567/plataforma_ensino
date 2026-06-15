from django.db import transaction

from assessments.domain.policies import validate_grade
from assessments.infrastructure.repositories import DjangoAssessmentRepository


@transaction.atomic
def record_grade(*, student, assessment, grade: float, date, repository=None):
    return (repository or DjangoAssessmentRepository()).record_grade(
        student=student,
        assessment=assessment,
        grade=validate_grade(grade),
        date=date,
    )
