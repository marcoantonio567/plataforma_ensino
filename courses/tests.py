from datetime import date

from django.test import TestCase

from courses.application.services import create_lesson, create_module
from courses.domain.value_objects import CargaHoraria, DuracaoAula, InvalidCourseValue
from courses.models import Curso, RegraCurso


class CourseServicesTest(TestCase):
    def setUp(self):
        self.course = Curso.objects.create(nome="DDD", carga_horaria=20)
        self.rule = RegraCurso.objects.create(curso=self.course, data_inicio=date.today())

    def test_modules_and_lessons_receive_sequential_order(self):
        first = create_module(self.course, name="Dominio")
        second = create_module(self.course, name="Aplicacao")
        lesson = create_lesson(
            self.course,
            first,
            title="Entidades",
            duration=30,
            content="",
        )

        self.assertEqual((first.ordem, second.ordem), (1, 2))
        self.assertEqual(lesson.ordem, 1)

    def test_course_returns_current_rule_for_date(self):
        old_rule = RegraCurso.objects.create(
            curso=self.course,
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 12, 31),
            media_minima=5.0,
        )
        current_rule = RegraCurso.objects.create(
            curso=self.course,
            data_inicio=date(2026, 1, 1),
            media_minima=7.0,
        )

        self.assertEqual(self.course.regra_vigente(date(2025, 6, 1)), old_rule)
        self.assertEqual(self.course.regra_vigente(date(2026, 6, 1)), current_rule)

    def test_course_value_objects_validate_and_compare_by_value(self):
        self.assertEqual(CargaHoraria(20), CargaHoraria("20"))
        self.assertEqual(DuracaoAula(30), DuracaoAula(30))

        with self.assertRaises(InvalidCourseValue):
            CargaHoraria(0)

        with self.assertRaises(Exception):
            DuracaoAula(30).valor = 45

    def test_course_aggregate_rejects_lesson_for_module_from_another_course(self):
        other_course = Curso.objects.create(nome="Outro", carga_horaria=10)
        other_module = create_module(other_course, name="Modulo externo")

        with self.assertRaises(ValueError):
            self.course.adicionar_aula(
                other_module,
                titulo="Aula externa",
                duracao=30,
                conteudo="",
                ordem=1,
            )
