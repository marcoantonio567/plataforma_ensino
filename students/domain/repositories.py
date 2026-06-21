from typing import Protocol


class EnrollmentRepository(Protocol):
    """Repository do aggregate root Matricula.

    Solicitacao, Aproveitamento, SegundaChamada, RevisaoNota e Equivalencia sao
    entidades internas da jornada academica e nao possuem repositories proprios.
    """

    def get_or_create_student(self, user): ...

    def find_by_student_and_course(self, student, course): ...

    def add(self, student, course): ...

    def save(self, enrollment, *, fields: list[str] | None = None) -> None: ...


StudentRepository = EnrollmentRepository
