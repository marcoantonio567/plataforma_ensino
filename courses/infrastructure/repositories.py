from django.db.models import Max

from courses.domain.policies import next_order
from courses.models import Aula, Curso, Modulo


class DjangoCourseRepository:
    def get(self, course_id: int):
        return Curso.objects.get(pk=course_id)

    def save(self, course, *, fields: list[str] | None = None) -> None:
        if fields is None:
            course.save()
        else:
            course.save(update_fields=fields)

    def next_module_order(self, course_id: int) -> int:
        maximum = Modulo.objects.filter(curso_id=course_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return next_order(maximum)

    def add_module_to_course(self, course, *, name: str, order: int):
        module = course.adicionar_modulo(nome=name, ordem=order)
        module.save()
        return module

    def next_lesson_order(self, module_id: int) -> int:
        maximum = Aula.objects.filter(modulo_id=module_id).aggregate(
            maximum=Max("ordem")
        )["maximum"]
        return next_order(maximum)

    def add_lesson_to_course(
        self,
        course,
        module,
        *,
        title: str,
        duration: int,
        content: str,
        order: int,
    ):
        lesson = course.adicionar_aula(
            module,
            titulo=title,
            duracao=duration,
            conteudo=content,
            ordem=order,
        )
        lesson.save()
        return lesson

    def remove_module_from_course(self, course_id: int, module_id: int) -> None:
        course = self.get(course_id)
        module = Modulo.objects.get(pk=module_id, curso=course)
        course.remover_modulo(module)

    def remove_lesson_from_course(self, course_id: int, lesson_id: int) -> None:
        course = self.get(course_id)
        lesson = Aula.objects.select_related("modulo").get(
            pk=lesson_id,
            modulo__curso=course,
        )
        course.remover_aula(lesson)
