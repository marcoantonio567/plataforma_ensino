from typing import Protocol


class CourseRepository(Protocol):
    """Repository do aggregate root Curso.

    Modulo e Aula sao entidades internas do agregado e, por isso, nao possuem
    repositories proprios.
    """

    def get(self, course_id: int): ...

    def save(self, course, *, fields: list[str] | None = None) -> None: ...

    def next_module_order(self, course_id: int) -> int: ...

    def add_module_to_course(self, course, *, name: str, order: int): ...

    def next_lesson_order(self, module_id: int) -> int: ...

    def add_lesson_to_course(
        self,
        course,
        module,
        *,
        title: str,
        duration: int,
        content: str,
        order: int,
    ): ...

    def remove_module_from_course(self, course_id: int, module_id: int) -> None: ...

    def remove_lesson_from_course(self, course_id: int, lesson_id: int) -> None: ...
