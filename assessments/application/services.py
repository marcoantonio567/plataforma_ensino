from django.db import transaction

from assessments.domain.policies import validate_grade
from assessments.infrastructure.repositories import DjangoAssessmentRepository


@transaction.atomic
def record_grade(*, student, assessment, grade: float, date, repository=None):
    return (repository or DjangoAssessmentRepository()).save_result_for_assessment(
        student=student,
        assessment=assessment,
        grade=validate_grade(grade),
        date=date,
    )
