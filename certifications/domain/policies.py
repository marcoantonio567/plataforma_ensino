from enum import StrEnum

from certifications.domain.services import CertificationDenied, validar_emissao_certificado


class CertificateStatus(StrEnum):
    ISSUED = "EMITIDO"
    SUSPENDED = "SUSPENSO"
    REVOKED = "REVOGADO"


def validate_certificate_issuance(
    enrollment,
    *,
    has_completed_required_project: bool,
    has_severe_integrity_incident: bool,
) -> None:
    return validar_emissao_certificado(
        enrollment,
        concluiu_projeto_obrigatorio=has_completed_required_project,
        possui_incidente_grave=has_severe_integrity_incident,
    )


def renewed_expiration(current_expiration, new_expiration=None):
    return new_expiration if new_expiration is not None else current_expiration


def issue_certificate(certificate, *, expiration=None):
    return certificate.emitir(validade=expiration)


def revoke_certificate(certificate):
    return certificate.revogar()


def suspend_certificate(certificate):
    return certificate.suspender()


def renew_certificate(certificate, *, new_expiration=None):
    return certificate.renovar(renewed_expiration(certificate.validade, new_expiration))
