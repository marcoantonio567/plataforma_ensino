from enum import StrEnum


class CertificateStatus(StrEnum):
    ISSUED = "EMITIDO"
    SUSPENDED = "SUSPENSO"
    REVOKED = "REVOGADO"


def renewed_expiration(current_expiration, new_expiration=None):
    return new_expiration if new_expiration is not None else current_expiration
