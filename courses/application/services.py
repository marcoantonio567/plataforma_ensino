from django.db import transaction

from courses.infrastructure.repositories import DjangoCourseRepository


@transaction.atomic
def create_module(course, *, name: str, repository=None):
    repository = repository or DjangoCourseRepository()
    return repository.add_module_to_course(
        course,
        name=name,
        order=repository.next_module_order(course.pk),
    )


@transaction.atomic
def create_lesson(course, module, *, title: str, duration: int, content: str, repository=None):
    repository = repository or DjangoCourseRepository()
    return repository.add_lesson_to_course(
        course,
        module,
        title=title,
        duration=duration,
        content=content,
        order=repository.next_lesson_order(module.pk),
    )


@transaction.atomic
def delete_module(course_id: int, module_id: int, repository=None):
    (repository or DjangoCourseRepository()).remove_module_from_course(course_id, module_id)


@transaction.atomic
def delete_lesson(course_id: int, lesson_id: int, repository=None):
    (repository or DjangoCourseRepository()).remove_lesson_from_course(course_id, lesson_id)
