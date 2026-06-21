from django.db import transaction

from certifications.domain.policies import (
    issue_certificate,
    renew_certificate,
    revoke_certificate,
    suspend_certificate,
)
from certifications.domain.services import validar_emissao_certificado
from certifications.infrastructure.repositories import DjangoCertificateRepository


@transaction.atomic
def issue(enrollment, expiration=None, repository=None):
    repository = repository or DjangoCertificateRepository()
    rule = enrollment.regra_curso
    minimum_grade = rule.media_minima if rule is not None else 0

    validar_emissao_certificado(
        enrollment,
        concluiu_projeto_obrigatorio=repository.has_completed_project(
            enrollment,
            minimum_grade=minimum_grade,
        ),
        possui_incidente_grave=repository.has_severe_integrity_incident(enrollment),
    )

    certificate = issue_certificate(
        repository.get_or_create_for_enrollment(enrollment, expiration=expiration),
        expiration=expiration,
    )
    repository.save(certificate, fields=["status", "validade"])
    return certificate


@transaction.atomic
def revoke(certificate, repository=None):
    revoke_certificate(certificate)
    (repository or DjangoCertificateRepository()).save(certificate, fields=["status"])
    return certificate


@transaction.atomic
def suspend(certificate, repository=None):
    suspend_certificate(certificate)
    (repository or DjangoCertificateRepository()).save(certificate, fields=["status"])
    return certificate


@transaction.atomic
def renew(certificate, new_expiration=None, repository=None):
    renew_certificate(certificate, new_expiration=new_expiration)
    (repository or DjangoCertificateRepository()).save(
        certificate,
        fields=["status", "validade"],
    )
    return certificate
