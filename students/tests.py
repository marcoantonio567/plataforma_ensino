from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from courses.models import Curso, RegraCurso
from students.application.services import (
    cancel_enrollment,
    enroll_student,
    get_or_create_student,
)
from students.domain.exceptions import InvalidEnrollmentTransition
from students.models import Matricula


class EnrollmentServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("student")
        self.student = get_or_create_student(self.user)
        self.course = Curso.objects.create(nome="Arquitetura", carga_horaria=10)
        self.rule = RegraCurso.objects.create(
            curso=self.course,
            data_inicio=timezone.localdate(),
            media_minima=7.0,
            carga_horaria_minima=10,
        )

    def test_enrollment_can_be_cancelled_and_reactivated(self):
        created = enroll_student(self.student, self.course)
        cancel_enrollment(created.enrollment)
        reactivated = enroll_student(self.student, self.course)

        self.assertTrue(created.created)
        self.assertEqual(created.enrollment.regra_curso, self.rule)
        self.assertTrue(reactivated.reactivated)
        self.assertEqual(reactivated.enrollment.status, Matricula.Status.ATIVA)

    def test_completed_enrollment_cannot_be_cancelled(self):
        result = enroll_student(self.student, self.course)
        enrollment = result.enrollment
        enrollment.concluir(media_final=8.0, carga_horaria_cumprida=10)

        with self.assertRaises(InvalidEnrollmentTransition):
            enrollment.cancelar()

    def test_enrollment_rejects_invalid_progress(self):
        enrollment = enroll_student(self.student, self.course).enrollment

        with self.assertRaises(InvalidEnrollmentTransition):
            enrollment.atualizar_progresso(120)
