from django.db import transaction

from certifications.domain.policies import CertificateStatus, renewed_expiration
from certifications.infrastructure.repositories import DjangoCertificateRepository


@transaction.atomic
def revoke(certificate, repository=None):
    certificate.status = CertificateStatus.REVOKED
    (repository or DjangoCertificateRepository()).save(certificate, fields=["status"])
    return certificate


@transaction.atomic
def suspend(certificate, repository=None):
    certificate.status = CertificateStatus.SUSPENDED
    (repository or DjangoCertificateRepository()).save(certificate, fields=["status"])
    return certificate


@transaction.atomic
def renew(certificate, new_expiration=None, repository=None):
    certificate.status = CertificateStatus.ISSUED
    certificate.validade = renewed_expiration(certificate.validade, new_expiration)
    (repository or DjangoCertificateRepository()).save(
        certificate,
        fields=["status", "validade"],
    )
    return certificate
