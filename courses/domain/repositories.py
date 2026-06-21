from typing import Protocol


class CourseRepository(Protocol):
    def next_module_order(self, course_id: int) -> int: ...

    def create_module(self, course, *, name: str, order: int): ...

    def next_lesson_order(self, module_id: int) -> int: ...

    def create_lesson(
        self,
        module,
        *,
        title: str,
        duration: int,
        content: str,
        order: int,
    ): ...

    def delete_module(self, course_id: int, module_id: int) -> None: ...

    def delete_lesson(self, course_id: int, lesson_id: int) -> None: ...
