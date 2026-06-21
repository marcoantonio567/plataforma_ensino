from django.db import transaction

from certifications.domain.policies import (
    issue_certificate,
    renew_certificate,
    revoke_certificate,
    suspend_certificate,
    validate_certificate_issuance,
)
from certifications.infrastructure.repositories import DjangoCertificateRepository


@transaction.atomic
def issue(enrollment, expiration=None, repository=None):
    repository = repository or DjangoCertificateRepository()
    rule = enrollment.regra_curso
    minimum_grade = rule.media_minima if rule is not None else 0

    validate_certificate_issuance(
        enrollment,
        has_completed_required_project=repository.has_completed_project(
            enrollment,
            minimum_grade=minimum_grade,
        ),
        has_severe_integrity_incident=repository.has_severe_integrity_incident(enrollment),
    )

    certificate = issue_certificate(
        repository.get_or_create(enrollment, expiration=expiration),
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
