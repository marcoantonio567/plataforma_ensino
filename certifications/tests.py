from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from assessments.models import Avaliacao, AvaliacaoRealizada, ProjetoPratico
from certifications.application.services import issue, renew, revoke, suspend
from certifications.domain.policies import CertificationDenied
from certifications.models import (
    Certificado,
    GravidadeIncidente,
    IncidenteIntegridade,
    StatusCertificado,
    TipoIncidente,
)
from courses.models import Curso, Modulo, RegraCurso
from students.models import Aluno, Matricula


class CertificateServicesTest(TestCase):
    def setUp(self):
        user = User.objects.create_user("certificate-student")
        self.student = Aluno.objects.create(
            usuario=user,
            numero_matricula="ALU0001",
            data_ingresso=date.today(),
        )
        self.course = Curso.objects.create(nome="Certificacao", carga_horaria=8)
        self.rule = RegraCurso.objects.create(
            curso=self.course,
            data_inicio=date.today(),
            media_minima=6.0,
            carga_horaria_minima=8,
        )
        self.enrollment = Matricula.objects.create(
            aluno=self.student,
            curso=self.course,
            regra_curso=self.rule,
            status=Matricula.Status.CONCLUIDA,
            media_final=8.0,
            carga_horaria_cumprida=8,
        )

    def test_certificate_lifecycle(self):
        certificate = Certificado.objects.create(matricula=self.enrollment)

        suspend(certificate)
        self.assertEqual(certificate.status, StatusCertificado.SUSPENSO)

        renew(certificate, date(2030, 1, 1))
        self.assertEqual(certificate.status, StatusCertificado.EMITIDO)
        self.assertEqual(certificate.validade, date(2030, 1, 1))

        revoke(certificate)
        self.assertEqual(certificate.status, StatusCertificado.REVOGADO)

    def test_issues_certificate_when_enrollment_meets_rule(self):
        certificate = issue(self.enrollment)

        self.assertEqual(certificate.matricula, self.enrollment)
        self.assertEqual(certificate.status, StatusCertificado.EMITIDO)

    def test_denies_certificate_when_grade_is_below_minimum(self):
        self.enrollment.media_final = 5.9
        self.enrollment.save(update_fields=["media_final"])

        with self.assertRaises(CertificationDenied):
            issue(self.enrollment)

    def test_denies_certificate_when_there_is_severe_integrity_incident(self):
        IncidenteIntegridade.objects.create(
            matricula=self.enrollment,
            tipo=TipoIncidente.FRAUDE,
            gravidade=GravidadeIncidente.GRAVE,
        )

        with self.assertRaises(CertificationDenied):
            issue(self.enrollment)

    def test_requires_completed_project_when_course_rule_demands_it(self):
        self.rule.exige_projeto_final = True
        self.rule.save(update_fields=["exige_projeto_final"])

        with self.assertRaises(CertificationDenied):
            issue(self.enrollment)

        module = Modulo.objects.create(curso=self.course, nome="Final", ordem=1)
        project = ProjetoPratico.objects.create(
            modulo=module,
            tipo=Avaliacao.Tipo.PROJETO_PRATICO,
            peso=1,
        )
        AvaliacaoRealizada.objects.create(
            aluno=self.student,
            avaliacao=project,
            nota=8.0,
            data=date.today(),
        )

        certificate = issue(self.enrollment)
        self.assertEqual(certificate.status, StatusCertificado.EMITIDO)
