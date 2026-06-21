from enum import StrEnum


class CertificateStatus(StrEnum):
    ISSUED = "EMITIDO"
    SUSPENDED = "SUSPENSO"
    REVOKED = "REVOGADO"


class CertificationDenied(ValueError):
    pass


def validate_certificate_issuance(
    enrollment,
    *,
    has_completed_required_project: bool,
    has_severe_integrity_incident: bool,
) -> None:
    rule = enrollment.regra_curso

    if rule is None:
        raise CertificationDenied("A matricula nao possui regra de curso vigente registrada.")

    if enrollment.status != "CONCLUIDA":
        raise CertificationDenied("A matricula precisa estar concluida para emitir certificado.")

    if enrollment.media_final is None:
        raise CertificationDenied("A matricula nao possui media final registrada.")

    if enrollment.media_final < rule.media_minima:
        raise CertificationDenied("A media final esta abaixo da media minima exigida.")

    if enrollment.carga_horaria_cumprida < rule.carga_horaria_minima:
        raise CertificationDenied("A carga horaria cumprida esta abaixo do minimo exigido.")

    if rule.exige_projeto_final and not has_completed_required_project:
        raise CertificationDenied("O projeto final obrigatorio ainda nao foi concluido.")

    if has_severe_integrity_incident:
        raise CertificationDenied("A matricula possui incidente grave de integridade academica.")


def renewed_expiration(current_expiration, new_expiration=None):
    return new_expiration if new_expiration is not None else current_expiration
