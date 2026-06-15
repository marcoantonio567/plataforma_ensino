from django.db.models import Max

from courses.models import Aula, Modulo


class DjangoCourseRepository:
    def next_module_order(self, course_id: int) -> int:
        maximum = Modulo.objects.filter(curso_id=course_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return (maximum or 0) + 1

    def next_lesson_order(self, module_id: int) -> int:
        maximum = Aula.objects.filter(modulo_id=module_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return (maximum or 0) + 1

    def delete_module(self, course_id: int, module_id: int) -> None:
        Modulo.objects.filter(pk=module_id, curso_id=course_id).delete()

    def delete_lesson(self, course_id: int, lesson_id: int) -> None:
        Aula.objects.filter(pk=lesson_id, modulo__curso_id=course_id).delete()
