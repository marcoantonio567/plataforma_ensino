from django.contrib.auth.models import User
from django.test import TestCase

from courses.models import Curso
from students.application.services import (
    cancel_enrollment,
    enroll_student,
    get_or_create_student,
)
from students.models import Matricula


class EnrollmentServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("student")
        self.student = get_or_create_student(self.user)
        self.course = Curso.objects.create(nome="Arquitetura", carga_horaria=10)

    def test_enrollment_can_be_cancelled_and_reactivated(self):
        created = enroll_student(self.student, self.course)
        cancel_enrollment(created.enrollment)
        reactivated = enroll_student(self.student, self.course)

        self.assertTrue(created.created)
        self.assertTrue(reactivated.reactivated)
        self.assertEqual(reactivated.enrollment.status, Matricula.Status.ATIVA)
