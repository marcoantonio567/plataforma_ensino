class InvalidGrade(ValueError):
    pass


def validate_grade(grade: float) -> float:
    grade = float(grade)
    if not 0 <= grade <= 10:
        raise InvalidGrade("A nota deve estar entre 0 e 10.")
    return grade
