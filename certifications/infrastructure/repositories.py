from assessments.models import Avaliacao, AvaliacaoRealizada
from certifications.models import Certificado, GravidadeIncidente, IncidenteIntegridade


class DjangoCertificateRepository:
    def get_or_create_for_enrollment(self, enrollment, *, expiration=None):
        certificate, _ = Certificado.objects.get_or_create(
            matricula=enrollment,
            defaults={"validade": expiration},
        )
        return certificate

    def has_completed_project(self, enrollment, *, minimum_grade: float) -> bool:
        return AvaliacaoRealizada.objects.filter(
            aluno=enrollment.aluno,
            avaliacao__modulo__curso=enrollment.curso,
            avaliacao__tipo=Avaliacao.Tipo.PROJETO_PRATICO,
            nota__gte=minimum_grade,
        ).exists()

    def has_severe_integrity_incident(self, enrollment) -> bool:
        return IncidenteIntegridade.objects.filter(
            matricula=enrollment,
            gravidade=GravidadeIncidente.GRAVE,
        ).exists()

    def save(self, certificate, *, fields: list[str] | None = None) -> None:
        if fields is None:
            certificate.save()
        else:
            certificate.save(update_fields=fields)
