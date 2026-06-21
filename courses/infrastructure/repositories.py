from django.db.models import Max

from courses.domain.policies import next_order
from courses.models import Aula, Modulo


class DjangoCourseRepository:
    def next_module_order(self, course_id: int) -> int:
        maximum = Modulo.objects.filter(curso_id=course_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return next_order(maximum)

    def create_module(self, course, *, name: str, order: int):
        return Modulo.objects.create(curso=course, nome=name, ordem=order)

    def next_lesson_order(self, module_id: int) -> int:
        maximum = Aula.objects.filter(modulo_id=module_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return next_order(maximum)

    def create_lesson(
        self,
        module,
        *,
        title: str,
        duration: int,
        content: str,
        order: int,
    ):
        return Aula.objects.create(
            modulo=module,
            titulo=title,
            duracao=duration,
            conteudo=content,
            ordem=order,
        )

    def delete_module(self, course_id: int, module_id: int) -> None:
        Modulo.objects.filter(pk=module_id, curso_id=course_id).delete()

    def delete_lesson(self, course_id: int, lesson_id: int) -> None:
        Aula.objects.filter(pk=lesson_id, modulo__curso_id=course_id).delete()
