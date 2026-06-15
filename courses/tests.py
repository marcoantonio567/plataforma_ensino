from datetime import date

from django.test import TestCase

from courses.application.services import create_lesson, create_module
from courses.models import Curso, RegraCurso


class CourseServicesTest(TestCase):
    def setUp(self):
        self.course = Curso.objects.create(nome="DDD", carga_horaria=20)
        self.rule = RegraCurso.objects.create(data_inicio=date.today())

    def test_modules_and_lessons_receive_sequential_order(self):
        first = create_module(self.course, name="Dominio")
        second = create_module(self.course, name="Aplicacao")
        lesson = create_lesson(
            first,
            title="Entidades",
            duration=30,
            content="",
        )

        self.assertEqual((first.ordem, second.ordem), (1, 2))
        self.assertEqual(lesson.ordem, 1)
