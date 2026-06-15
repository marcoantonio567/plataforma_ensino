from typing import Protocol


class AssessmentRepository(Protocol):
    def record_grade(self, *, student, assessment, grade: float, date): ...
