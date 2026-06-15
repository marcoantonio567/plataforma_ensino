from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from certifications.application.services import renew, revoke, suspend
from certifications.models import Certificado, StatusCertificado
from courses.models import Curso
from students.models import Aluno, Matricula


class CertificateServicesTest(TestCase):
    def setUp(self):
        user = User.objects.create_user("certificate-student")
        student = Aluno.objects.create(
            usuario=user,
            numero_matricula="ALU0001",
            data_ingresso=date.today(),
        )
        course = Curso.objects.create(nome="Certificacao", carga_horaria=8)
        enrollment = Matricula.objects.create(aluno=student, curso=course)
        self.certificate = Certificado.objects.create(matricula=enrollment)

    def test_certificate_lifecycle(self):
        suspend(self.certificate)
        self.assertEqual(self.certificate.status, StatusCertificado.SUSPENSO)

        renew(self.certificate, date(2030, 1, 1))
        self.assertEqual(self.certificate.status, StatusCertificado.EMITIDO)
        self.assertEqual(self.certificate.validade, date(2030, 1, 1))

        revoke(self.certificate)
        self.assertEqual(self.certificate.status, StatusCertificado.REVOGADO)
