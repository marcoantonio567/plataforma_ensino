from django.db import transaction

from courses.infrastructure.repositories import DjangoCourseRepository


@transaction.atomic
def create_module(course, *, name: str, repository=None):
    repository = repository or DjangoCourseRepository()
    return repository.create_module(
        course,
        name=name,
        order=repository.next_module_order(course.pk),
    )


@transaction.atomic
def create_lesson(module, *, title: str, duration: int, content: str, repository=None):
    repository = repository or DjangoCourseRepository()
    return repository.create_lesson(
        module,
        title=title,
        duration=duration,
        content=content,
        order=repository.next_lesson_order(module.pk),
    )


@transaction.atomic
def delete_module(course_id: int, module_id: int, repository=None):
    (repository or DjangoCourseRepository()).delete_module(course_id, module_id)


@transaction.atomic
def delete_lesson(course_id: int, lesson_id: int, repository=None):
    (repository or DjangoCourseRepository()).delete_lesson(course_id, lesson_id)
