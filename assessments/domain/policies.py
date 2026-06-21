from assessments.domain.value_objects import InvalidGrade, Nota


def validate_grade(grade: float) -> float:
    return float(Nota(grade))
